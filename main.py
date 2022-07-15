from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen, ScreenManager, RiseInTransition
import svgwrite

figure = 0
state = None
pos1 = None
el = None
color = [1,1,1,1]
names = ["Line", "Path", "Rectangle", "Circle", "Text", "Cursor"]
filled = False
colorHistory=[]
colorUndo=[]
objects = []
undolist = []
lin = None
class Painter(Widget):
	def on_touch_down(self, touch):
		global state, pos1, el, color, objects, undolist, colorHistory, colorUndo, lin
		if figure == 1:
			with self.canvas:
				Color(0, 1, 1, 0.75)
				d = 30.
				el = Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
				Color().rgba = color
				if state != "exist":
					lin = Line(width=3, points=(touch.x, touch.y))
					print(lin)
				else:
					print(lin)
					lin.points += [touch.x, touch.y]
				if state== None:
					state="exist"
		if state == None:
			state = "pos1"
			pos1 = (touch.x, touch.y)
		elif state == "pos1":
			state = "pos2"
		with self.canvas:
			if state == "pos1":
				Color(0, 1, 1, 0.75)
				d = 30.
				el = Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
			if state == "pos2":
				undolist.clear()
				Color().rgba = color
				print(color)
				if figure==0:
					objects.append([Line(points=(pos1[0], pos1[1], touch.x, touch.y), width=2), color])
				elif figure == 2:
					if filled:
						objects.append([Rectangle(pos=(pos1[0], pos1[1]), size=(touch.x-pos1[0], touch.y-pos1[1])), color])
					else:
						objects.append([Line(width=3, rectangle=(pos1[0], pos1[1], touch.x-pos1[0], touch.y-pos1[1])), color])
				elif figure == 3:
					if filled:
						objects.append([Ellipse(pos=(pos1[0], pos1[1]), size=(touch.x-pos1[0], touch.y-pos1[1])), color])
					else:
						objects.append([Line(width=3, ellipse=(pos1[0], pos1[1], touch.x-pos1[0], touch.y-pos1[1])), color])
				print(objects)
				state = None
				self.canvas.remove(el)
	def undo(self, obj):
		global undolist
		try:
			item = objects.pop(-1)
			undolist.append(item)
			self.canvas.remove(item[0])
		except:
			pass
	def redo(self, obj):
		 global objects
		 try:
		 	item = undolist.pop(-1)
		 	objects.append(item)
		 	print(item[1])
		 	self.canvas.add(Color(rgba=item[1]))
		 	self.canvas.add(item[0])
		 except:
		 	pass
		 
class PaintApp(App):
	def build(self):
		self.sm = ScreenManager(transition=RiseInTransition())
		self.mainScreen = Screen(name="main")
		self.paintMenu = Screen(name="painter")
		self.sm.switch_to(self.mainScreen)
	
		mainScreen_layout = BoxLayout(orientation="vertical")
		newBt = Button(text="New")
		newBt.bind(on_release=self.newFile)
		mainScreen_layout.add_widget(newBt)
		mainScreen_layout.add_widget(Button(text="Open"))
		self.mainScreen.add_widget(mainScreen_layout) 
		self.painter = Painter()
		spinner = Spinner(text=names[figure],values=tuple(names))
		spinner.bind(text=self.get_spinner_selection)
		bl1 = BoxLayout(orientation ="vertical")
		bl2 = BoxLayout(orientation ="horizontal", size_hint=(1, 0.15))
		clrBt = Button(text="Clear")
		clrBt.bind(on_release=self.cls)
		propBt = Button(text="Properties")
		propBt.bind(on_release=self.drawProperties)
		objHistory=BoxLayout(orientation="vertical", size_hint=(0.5, 1))
		undoBt = Button(text="Undo")
		undoBt.bind(on_release=self.painter.undo)
		redoBt = Button(text="Redo")
		redoBt.bind(on_release=self.painter.redo)
		bl2.add_widget(clrBt)
		bl2.add_widget(spinner) 
		bl2.add_widget(propBt)
		objHistory.add_widget(undoBt)
		objHistory.add_widget(redoBt)
		bl2.add_widget(objHistory)
		bl1.add_widget(self.painter)
		bl1.add_widget(bl2)
		self.paintMenu.add_widget(bl1)
		
		return self.sm
	def newFile(self, instance):
		self.sm.switch_to(self.paintMenu)
		file = svgwrite.Drawing("new.svg")
	def changeColor(self, instance, value):
		global color
		color = value
	def cls(self, obj):
	    global state, pos1, objects, undolist
	    state = None
	    objects = undolist = []
	    pos1 = None
	    self.painter.canvas.clear()
	def drawProperties(self, obj):
		global col
		col = ColorPicker()
		col.color = color
		backBt = Button(text="Back", size_hint=(1, 0.25))
		layout = BoxLayout(orientation="vertical")
		layout.add_widget(col)
		if figure != 0 and figure != 1:
			fillFigure = BoxLayout(orientation="horizontal", size_hint=(1, 0.25))
			fillFigureLabel = Label(text="Filled")
			fillFigureBox = CheckBox(active=filled)
			fillFigureBox.bind(active=self.fillFigureChange)
			fillFigure.add_widget(fillFigureLabel)
			fillFigure.add_widget(fillFigureBox)
			layout.add_widget(fillFigure)
		layout.add_widget(backBt)
		popup = Popup(title='Test popup',  content=layout,auto_dismiss=False, size_hint=(0.8, 0.9))
		col.bind(color=self.changeColor)
		backBt.bind(on_release=popup.dismiss)
		popup.open()
	def get_spinner_selection(self, spinner, text):
		global figure
		figure = names.index(text)
		state = None
		pos1 = None
	def fillFigureChange(self, checkbox, value):
		global filled
		if value:
			filled = True
		else:
			filled = False
if __name__ == '__main__':
    PaintApp().run()