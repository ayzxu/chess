from cmu_graphics import *

def onAppStart(app):
    app.message = "Hello from cmu_graphics!"
    app.counter = 0

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='lightblue')
    drawLabel(app.message, app.width//2, app.height//2, 
              font='Arial', size=24, bold=True)
    drawLabel(f"Counter: {app.counter}", app.width//2, app.height//2 + 50,
              font='Arial', size=16)

def onMousePress(app, mouseX, mouseY):
    app.counter += 1

def main():
    runApp(width=400, height=300)

if __name__ == '__main__':
    main() 