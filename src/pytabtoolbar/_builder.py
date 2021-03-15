import json

from typing import Any, Dict, List

from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMenu, QToolButton, QWidget

from .subgroup import ActionParams, Align
from .tabtoolbar import TabToolbar


class Builder(QtCore.QObject):
    def __init__(self, parent: QWidget):
        super(Builder, self).__init__(parent)
        self.parent: QWidget = parent
        self.guiWidgets: Dict[str, QWidget] = {}
        self.customWidgetCreators: Dict[str, QWidget] = {}

    def __getitem__(self, widget_name):
        if len(self.guiWidgets) > 0:
            if widget_name in self.guiWidgets:
                return self.guiWidgets[widget_name]
        raise Exception(
            "Builder does not contain a widget named '{}'".format(widget_name)
        )

    def read_json(self, json: Any, key: str, default: Any = None) -> Any:
        if json and key in json:
            return json[key]
        else:
            if default:
                return default
        raise Exception("JSON Key not found and no default specified")

    def set_widgetcreator(self, name: str, creator: QWidget):
        self.customWidgetCreators[name] = creator

    def create_tabtoolbar(self, config_path: str) -> TabToolbar:
        actions: List[QtCore.QObject] = self.parent.findChildren(QAction)
        menus: List[QtCore.QObject] = self.parent.findChildren(QMenu)
        self.actionsMap: Dict[str, QAction] = {}
        self.menusMap: Dict[str, QMenu] = {}
        for action in actions:
            self.actionsMap[action.objectName()] = action
        for menu in menus:
            self.menusMap[menu.objectName()] = menu

        configfile = QtCore.QFile(config_path)
        configfile.open(QtCore.QIODevice.ReadOnly)

        # configFile = Path(configPath)
        # if not configFile.exists():
        #    # TODO: raise error
        config: Any = None
        config = bytes(configfile.readAll()).decode()
        config = json.loads(config)
        # with open(configFile) as f:
        #    config = json.load(f)
        group_height: int = self.read_json(config, "groupHeight")
        group_rowcount: int = self.read_json(config, "groupRowCount")
        has_specialtab: bool = self.read_json(config, "specialTab")
        tt = TabToolbar(self.parent, group_height, group_rowcount)
        corner_actions: List = self.read_json(config, "cornerActions", {})
        for corner_action in corner_actions:
            tt.add_corneraction(self.actionsMap[corner_action])

        menuslist: List = self.read_json(config, "menus", {})
        for menuobject in menuslist:
            menu: QMenu = QMenu(self.parent)
            menu.setObjectName(self.read_json(menuobject, "name"))
            self.menusMap[menu.objectName()] = menu
            self.guiWidgets[menu.objectName()] = menu
            menuactions: List = self.read_json(menuobject, "actions", {})
            for action_name in menuactions:
                if action_name == "separator":
                    menu.addSeparator()
                else:
                    menu.addActions({self.actionsMap[action_name]})
        tabs = self.read_json(config, "tabs", {})
        for tab in tabs:
            page_displayname = self.read_json(tab, "displayName")
            page_name = self.read_json(tab, "name")
            page = tt.add_page(page_displayname)
            self.guiWidgets[page_name] = page
            groups = self.read_json(tab, "groups", {})
            for group_object in groups:
                group_displayname = self.read_json(group_object, "displayName")
                group_name = self.read_json(group_object, "name")
                group = page.add_group(group_displayname)
                self.guiWidgets[group_name] = group
                content = self.read_json(group_object, "content", {})
                for item in content:
                    # defaultTypes = {"action", "subgroup", "seperator"}
                    item_type = self.read_json(item, "itemType")
                    if item_type == "action":
                        params = self.create_actionparams(tt, item)
                        if params:
                            group.add_action(params.type, params.action, params.menu)
                    elif item_type == "subgroup":
                        align: Align = Align.Yes
                        aligned = self.read_json(item, "aligned", None)
                        if not aligned:
                            align = Align.No
                        subgroup = group.add_subgroup(align)
                        subgroup_name = self.read_json(item, "name")
                        self.guiWidgets[subgroup_name] = subgroup

                        subgroup_content = self.read_json(item, "content", {})
                        for subgroup_item in subgroup_content:
                            subgroup_itemtype = self.read_json(
                                subgroup_item, "itemType"
                            )
                            if subgroup_itemtype == "action":
                                params: ActionParams = self.create_actionparams(
                                    tt, subgroup_item
                                )
                                subgroup.add_action(
                                    params.type, params.action, params.menu
                                )
                            elif subgroup_itemtype == "horizontalActions":
                                h_actions = []
                                h_actionsarray = subgroup_item["actions"]

                                for h_action in h_actionsarray:
                                    h_actions.append(
                                        self.create_actionparams(tt, h_action)
                                    )
                                subgroup.add_hbuttons(h_actions)
                            else:
                                w = self.create_customwidget(
                                    tt, subgroup_itemtype, subgroup_item
                                )

                                subgroup.add_widget(w)
                    elif item_type == "separator":
                        group.add_separator()
                    else:
                        w = self.create_customwidget(tt, item_type, item)
                        group.add_widget(w)
        tt.set_specialtabenabled(has_specialtab)
        return tt

    def create_customwidget(self, tt: TabToolbar, name: str, item: Any) -> QWidget:

        if name not in self.customWidgetCreators:
            raise Exception("No Creator for '{}'".format(name))

        w = self.customWidgetCreators[name]
        w = w()
        if "name" in item:
            w.setObjectName(item["name"])
            self.guiWidgets[w.objectName()] = w
        w.setParent(tt)
        return w

    def create_actionparams(self, tt, obj: Any) -> ActionParams:
        params: ActionParams = ActionParams()

        type: str = obj["type"]
        if type == "delayedPopup":
            params.type = QToolButton.DelayedPopup
        elif type == "instantPopup":
            params.type = QToolButton.InstantPopup
        elif type == "menuButtonPopup":
            params.type = QToolButton.MenuButtonPopup
        else:
            # TODO: should throw error
            return params

        params.action = self.actionsMap[obj["name"]]
        if "menu" in obj and obj["menu"] is not None:
            params.menu = self.menusMap[obj["menu"]]
        return params
