
import sys, cv2
import numpy as np
import traceback

from cv2.typing import MatLike
from PySide6.QtWidgets import QApplication, QSizePolicy, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QFrame, QLabel, QSlider, QStatusBar
from PySide6.QtCore import Qt, QSize, QPointF
from PySide6.QtGui import QImage, QPixmap, QMouseEvent, QWheelEvent

CONTROL_NAME = ["Control 1", "Control 2", "Control 3", "Control 4"]
MAXIMUM_VALUES = [10, 10, 10, 10]
MINIMUM_VALUES = [0, 0, 0, 0]

def load_image() -> MatLike | None:
    return np.zeros((1,1,3), np.uint8)

def change_control(image:MatLike, param1:int, param2:int, param3:int, param4:int) -> MatLike:
    return image


class MainWindow(object):
    def __init__(self):
        self.metric1:QLabel
        self.metric2:QLabel
        self.metric3:QLabel
        self.metric4:QLabel
        self.slider1:QSlider
        self.slider2:QSlider
        self.slider3:QSlider
        self.slider4:QSlider
        self.graphicsView:QGraphicsView
        self.image:MatLike
    
    def setupUi(self, MainWindow: QMainWindow):
        self.main_window = MainWindow
        MainWindow.resize(1280, 740)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setSizeAdjustPolicy(QGraphicsView.SizeAdjustPolicy.AdjustToContents)
        self.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.graphicsView.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        self.verticalLayout.addWidget(self.graphicsView)

        self.frame = QFrame(self.centralwidget)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)

        elementos = [("metric1", "slider1"), ("metric2", "slider2"), ("metric3", "slider3"), ("metric4", "slider4")]

        def process_image(_:int) -> None:
            value1 = self.slider1.value()
            value2 = self.slider2.value()
            value3 = self.slider3.value()
            value4 = self.slider4.value()
            self.metric1.setText(CONTROL_NAME[0] + ": " + str(value1))
            self.metric2.setText(CONTROL_NAME[1] + ": " + str(value2))
            self.metric3.setText(CONTROL_NAME[2] + ": " + str(value3))
            self.metric4.setText(CONTROL_NAME[3] + ": " + str(value4))
            if hasattr(self, "image"):
                try:
                    processed = change_control(self.image, value1, value2, value3, value4)
                    self.show_image(processed)
                except Exception as e:
                    self.statusbar.showMessage(str(e), 20000)
                    print(traceback.format_exc())
                    QMessageBox.critical(MainWindow, "Error!", traceback.format_exc(), QMessageBox.StandardButton.Ok)
            
        
        for index, (metric_name, slider_name) in enumerate(elementos):
            frame = QFrame(self.frame)
            frame.setFrameShape(QFrame.Shape.StyledPanel)
            frame.setFrameShadow(QFrame.Shadow.Raised)
            frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            layout = QHBoxLayout(frame)

            label = QLabel(frame)
            label.setText(CONTROL_NAME[index])
            label.setMinimumSize(QSize(200, 0))
            setattr(self, metric_name, label)
            layout.addWidget(label)

            slider = QSlider(frame)
            slider.setMaximum(MAXIMUM_VALUES[index])
            slider.setMinimum(MINIMUM_VALUES[index])
            slider.setOrientation(Qt.Orientation.Horizontal)
            slider.setTickPosition(QSlider.TickPosition.TicksAbove)
            slider.valueChanged.connect(process_image)
            setattr(self, slider_name, slider)
            layout.addWidget(slider)

            self.verticalLayout_2.addWidget(frame)

        self.verticalLayout.addWidget(self.frame)

        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setStatusBar(self.statusbar)
        
        self.image = np.zeros((1, 1, 3), dtype=np.uint8)
        self.scene: QGraphicsScene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        pixmap: QPixmap = self.cv2_to_qpixmap(self.image)
        self.image_item: QGraphicsPixmapItem = QGraphicsPixmapItem(pixmap)
        self.graphicsView.setSceneRect(self.image_item.boundingRect())
        self.scene.addItem(self.image_item)
        self.graphicsView.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)
        
        def zoomEvent(event: QWheelEvent):
            if event.angleDelta().y() > 0:
                self.graphicsView.scale(1.20, 1.20)
            else:
                self.graphicsView.scale(0.8, 0.8)
        
        self._middle_mouse_pressed:bool = False
        self._middle_mouse_position_pressed:QPointF = QPointF(0,0)
        
        def releaseEvent(event: QMouseEvent) -> None:
            if event.button() == Qt.MouseButton.MiddleButton:
                self._middle_mouse_pressed = False
        
        def pressEvent(event: QMouseEvent):
            if event.button() == Qt.MouseButton.MiddleButton:
                self._middle_mouse_pressed = True
                self._middle_mouse_position_pressed = event.position()
        
        def mouseMoveEvent(event: QMouseEvent):
            if self._middle_mouse_pressed:
                delta = event.position() - self._middle_mouse_position_pressed
                self._middle_mouse_position_pressed = event.position()
                diffx = self.graphicsView.horizontalScrollBar().value() - delta.x()
                diffy = self.graphicsView.verticalScrollBar().value() - delta.y()
                self.graphicsView.horizontalScrollBar().setValue(int(diffx))
                self.graphicsView.verticalScrollBar().setValue(int(diffy))
        
        self.graphicsView.wheelEvent = zoomEvent
        self.graphicsView.mousePressEvent = pressEvent
        self.graphicsView.mouseReleaseEvent = releaseEvent
        self.graphicsView.mouseMoveEvent = mouseMoveEvent
    
    def show_image(self, cv_img:MatLike) -> None:
        pixmap: QPixmap = self.cv2_to_qpixmap(cv_img)
        self.image_item.setPixmap(pixmap)
        self.graphicsView.setSceneRect(pixmap.rect())
        self.graphicsView.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)
    
    @classmethod
    def cv2_to_qpixmap(cls, cv_img:MatLike) -> QPixmap:
        rgb_image:MatLike = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB) 
        h: int
        w: int
        ch: int
        h, w, ch = rgb_image.shape
        bytes_per_line: int = ch * w
        q_image: QImage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap: QPixmap = QPixmap.fromImage(q_image)
        return pixmap



def show():
    app = QApplication(sys.argv)
    ui = QMainWindow()
    main_window = MainWindow()
    main_window.setupUi(ui)
    ui.show()
    
    result = load_image()
    if result is not None:
        main_window.image = result
        main_window.show_image(main_window.image)
    else:
        main_window.statusbar.showMessage("Can't show imagem!")
    sys.exit(app.exec())


if __name__ == "__main__":
    show()