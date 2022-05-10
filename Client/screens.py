from vars import widget


def change_window(name, windows, *args):
    if name == "room":
        widget.addWidget(windows["room"](*args))
        widget.setCurrentIndex(widget.currentIndex() + 1)
    elif name == "login":
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(windows["login"](*args))
    elif name == "forgot":
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(windows["forgot"](*args))
    elif name == "signup":
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(windows["signup"](*args))
    elif name == "lobby":
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(windows["lobby"](*args))