import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QMessageBox, QVBoxLayout, QWidget, \
    QLineEdit, QPushButton, QHBoxLayout, QTextBrowser, QMenu, QAction, QInputDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem

storys_path = "Scripts/storys.xml"
storysCG_path = "Scripts/storysCG.xml"
storysPY_path = "Scripts/storysPY.xml"
maps_path = "Scripts/maps.xml"
roles_path = "Scripts/roles.xml"
skills_path = "Scripts/skills.xml"


class XmlEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML Editor")
        self.setGeometry(500, 300, 1000, 600)

        # 窗口布局
        main_layout = QVBoxLayout()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        layout_h1 = QHBoxLayout()
        layout_h2 = QHBoxLayout()
        layout_h3 = QHBoxLayout()
        main_layout.addLayout(layout_v1)
        main_layout.addLayout(layout_h1)
        main_layout.addLayout(layout_h2)
        main_layout.addLayout(layout_h3)
        central_widget.setLayout(main_layout)

        # 树状图
        self.tree = None
        self.mapsmodel = QStandardItemModel()
        self.eventmodel = QStandardItemModel()
        self.commonmodel = QStandardItemModel()
        self.storysmodel = QStandardItemModel()
        self.storysCGmodel = QStandardItemModel()
        self.storysPYmodel = QStandardItemModel()
        self.treeView1 = QTreeView(self)
        self.treeView1.setIndentation(10)
        self.treeView1.setFixedWidth(200)
        self.treeView2 = QTreeView(self)
        self.treeView2.setFixedWidth(200)
        self.treeView3 = QTreeView(self)

        self.treeView2.setModel(self.eventmodel)

        text_browser = QTextBrowser()
        text_browser.setFixedWidth(200)
        text_browser.setReadOnly(False)  # 允许编辑
        layout_v2.addWidget(text_browser)
        layout_v2.addWidget(self.treeView2)
        nested_widget = QWidget()
        nested_widget.setLayout(layout_v2)
        nested_widget.setFixedWidth(200)
        layout_h3.addWidget(self.treeView1)
        layout_h3.addWidget(nested_widget)
        layout_h3.addWidget(self.treeView3)

        self.storysmodel.itemChanged.connect(self.auto_save)

        # 搜索栏
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("搜索 story 的 name 值...")
        # search_bar.textChanged.connect(self.search_story)
        layout_v1.addWidget(search_bar)

        # 按钮
        story_button = QPushButton("地图")
        story_button.clicked.connect(lambda: self.treeView1.setModel(self.mapsmodel))
        story_button.setFixedSize(120, 40)
        layout_h1.addWidget(story_button)

        story_button = QPushButton("门派")
        story_button.clicked.connect(self.load_story)
        story_button.setFixedSize(120, 40)
        layout_h1.addWidget(story_button)

        story_button = QPushButton("物品")
        story_button.clicked.connect(self.load_story)
        story_button.setFixedSize(120, 40)
        layout_h1.addWidget(story_button)

        story_button = QPushButton("触发")
        story_button.clicked.connect(self.load_story)
        story_button.setFixedSize(120, 40)
        layout_h1.addWidget(story_button)

        story_button = QPushButton("storys")
        story_button.clicked.connect(lambda: self.treeView3.setModel(self.storysmodel))
        story_button.setFixedSize(120, 40)
        layout_h1.addWidget(story_button)

        story_button = QPushButton("storysPY")
        story_button.clicked.connect(lambda: self.treeView3.setModel(self.storysPYmodel))
        story_button.setFixedSize(120, 40)
        layout_h1.addWidget(story_button)

        story_button = QPushButton("storysCG")
        story_button.clicked.connect(lambda: self.treeView3.setModel(self.storysCGmodel))
        story_button.setFixedSize(120, 40)
        layout_h1.addWidget(story_button)

        story_button = QPushButton("角色")
        story_button.clicked.connect(lambda: self.load_story("story.xml"))
        story_button.setFixedSize(120, 40)
        layout_h2.addWidget(story_button)

        story_button = QPushButton("内功")
        story_button.clicked.connect(lambda: self.load_story("story.xml"))
        story_button.setFixedSize(120, 40)
        layout_h2.addWidget(story_button)

        story_button = QPushButton("外功")
        story_button.clicked.connect(lambda: self.load_story("story.xml"))
        story_button.setFixedSize(120, 40)
        layout_h2.addWidget(story_button)

        story_button = QPushButton("奥义")
        story_button.clicked.connect(lambda: self.load_story("story.xml"))
        story_button.setFixedSize(120, 40)
        layout_h2.addWidget(story_button)

        story_button = QPushButton("天赋")
        story_button.clicked.connect(lambda: self.load_story("story.xml"))
        story_button.setFixedSize(120, 40)
        layout_h2.addWidget(story_button)

        story_button = QPushButton("称号")
        story_button.clicked.connect(lambda: self.load_story("story.xml"))
        story_button.setFixedSize(120, 40)
        layout_h2.addWidget(story_button)

        story_button = QPushButton("战斗")
        story_button.clicked.connect(lambda: self.load_story("story.xml"))
        story_button.setFixedSize(120, 40)
        layout_h2.addWidget(story_button)

        layout_h1.addStretch()
        layout_h2.addStretch()

        # 初始化
        self.load_story(self.storysmodel, storys_path)
        self.load_story(self.storysCGmodel, storysPY_path)
        self.load_story(self.storysPYmodel, storysCG_path)

    def load_story(self, model, file_path):
        try:
            self.tree = ET.parse(file_path)
            root = self.tree.getroot()
            model.setHorizontalHeaderLabels([file_path.split('/')[1]])

            for story in root.findall("story"):
                label = story.get('name')
                story_item = QStandardItem(label)
                story_item.setData(label, role=2)
                story_item.setData(len(story), role=1)  # 存储子标签个数
                story_item.setEditable(True)
                model.appendRow(story_item)
                for i, child in enumerate(story):
                    label = f"{child.get('type')},{child.get('value')}"
                    child_item = QStandardItem(label)
                    child_item.setData(label, role=2)
                    child_item.setData(i, role=1)  # 存储子标签的位置
                    child_item.setEditable(True)
                    story_item.appendRow(child_item)
                    if list(child):
                        for condition in child:
                            label = f"{condition.tag},{condition.get('type')},{condition.get('value')}"
                            condition_item = QStandardItem(label)
                            condition_item.setData(label)
                            child_item.appendRow(condition_item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"加载 story文件 失败: {str(e)}")

    def load_maps(self):
        try:
            self.tree = ET.parse(maps_path)
            root = self.tree.getroot()
            self.mapsmodel.clear()
            self.mapsmodel.setHorizontalHeaderLabels(["maps"])
            map_unit_map = {}
            bigmap_list = []
            for map in root.findall("map"):
                if len(map) <= 1 or map[1].get('x') == "-1":
                    label = map.get('name')
                    map_unit_item = QStandardItem(label)
                    map_unit_item.setData(label)
                    map_unit_map[label] = map_unit_item
                    for i, mapunit in enumerate(map.findall("mapunit")):
                        label = mapunit.get('name')
                        mapunit_item = QStandardItem(label)
                        mapunit_item.setData(label, role=2)
                        mapunit_item.setData(i, role=1)
                        map_unit_item.appendRow(mapunit_item)
                else:
                    bigmap_list.append(map)
            for bigmap in bigmap_list:
                label = bigmap.get('name')
                bigmap_item = QStandardItem(label)
                bigmap_item.setData(label, role=2)
                self.mapsmodel.appendRow(bigmap_item)
                for i, mapunit in enumerate(bigmap.findall("mapunit")):
                    label = mapunit.get('name')
                    map_unit = map_unit_map.get(label)
                    if map_unit:
                        bigmap_item.appendRow(map_unit)
                    else:
                        self.mapsmodel.appendRow(map_unit)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"加载 XML 失败: {str(e)}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # 只监听左键点击
            print(1)

            # 检查点击的是哪个 `QTreeView`
            if self.treeView1.viewport().rect().contains(event.pos()):
                tree_view = self.treeView1
                model = self.mapsmodel
            elif self.treeView2.viewport().rect().contains(event.pos()):
                tree_view = self.treeView2
                model = self.eventmodel
            elif self.treeView3.viewport().rect().contains(event.pos()):
                tree_view = self.treeView3
                model = self.storysmodel
            else:
                return  # 如果点击在其他地方，不执行后续操作

            # 获取点击位置的索引
            index = tree_view.indexAt(event.pos())

            # 确保索引有效，并且是子项（有父节点）
            # if index.isValid() and index.parent().isValid():
            item = model.itemFromIndex(index)
            print(f"左键点击了子项: {item.text()}")

    def contextMenuEvent(self, event):
        index = self.treeView.indexAt(event.pos())  # 获取鼠标点击的项
        # 先检查索引是否有效
        if not index.isValid():
            return  # 如果索引无效，直接返回，避免闪退
        # 再检查是否是子项（即父节点存在）
        if index.parent().isValid():
            menu = QMenu(self)
        # 添加菜单项
        edit_action = QAction("编辑", self)
        delete_action = QAction("删除", self)
        rename_action = QAction("重命名", self)

        # 绑定事件
        edit_action.triggered.connect(self.edit_item)
        delete_action.triggered.connect(self.delete_item)
        rename_action.triggered.connect(self.rename_item)

        # 添加到菜单
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addAction(rename_action)

        # 显示菜单
        menu.exec_(event.globalPos())

    # 操作函数
    def edit_item(self):
        selected = self.treeView.selectedIndexes()
        if selected:
            item = self.storysmodel.itemFromIndex(selected[0])
            item.setEditable(True)  # 让该项变为可编辑

    def delete_item(self):
        selected = self.treeView.selectedIndexes()
        if selected:
            item = self.storysmodel.itemFromIndex(selected[0])
            parent = item.parent()
            if parent:
                parent.removeRow(item.row())
            else:
                self.storysmodel.removeRow(item.row())

    def rename_item(self):
        selected = self.treeView.selectedIndexes()
        if selected:
            item = self.storysmodel.itemFromIndex(selected[0])
            new_name, ok = QInputDialog.getText(self, "重命名", "输入新名称:")
            if ok and new_name:
                item.setText(new_name)
                self.auto_save(item)  # 自动保存新名称

    def auto_save(self, item, file_path):
        """自动更新 XML 文件"""
        self.tree = ET.parse(file_path)
        root = self.tree.getroot()
        updated_text = item.text()  # 获取修改后的文本
        if not item.parent():
            target_story = root.find(f"story[@name='{item.data()}']")
            if target_story is not None:
                target_story.set("name", updated_text)
                self.storysmodel.itemChanged.disconnect(self.auto_save)  # 暂时断开信号
                item.setData(updated_text)
                self.storysmodel.itemChanged.connect(self.auto_save)  # 重新连接信号
                self.tree.write(file_path, encoding="utf-8", xml_declaration=True)  # 保存更改
                print("修改成功")
            else:
                print("未找到匹配的story")
        else:
            print(root)
            target_story = root.find(f"story[@name='{item.parent().data()}']")
            if target_story is not None:
                parts = item.data().split(',')
                tag = parts[0]
                type = parts[1].split('=')[1]
                value = parts[2].split('=')[1]
                print(type)
                print(value)
                target_child = target_story.find(f"action[@type='{type}' and @value='{value}']")
                print(target_child)
                parts = updated_text.split(',')
                tag = parts[0]
                type = parts[1].split('=')[1]
                value = parts[2].split('=')[1]
                target_child.set("type", type)
                target_child.set("value", value)
                self.storysmodel.itemChanged.disconnect(self.auto_save)  # 暂时断开信号
                item.setData(updated_text)
                self.storysmodel.itemChanged.connect(self.auto_save)  # 重新连接信号
                self.tree.write("story.xml", encoding="utf-8", xml_declaration=True)  # 保存更改
                print("修改成功")
            else:
                print("未找到匹配的story")

    def my(self):
        print(10)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = XmlEditor()
    editor.show()
    sys.exit(app.exec_())
