
def onclick():
    print("print from One Click Callback")

def registerClick(callback, x, y):
    print(f"Print from registerClick x: {x} & y: {y}")
    callback()

registerClick(onclick, 'hello', 'world')

