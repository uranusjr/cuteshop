MKDIR = mkdir

win32 {
    COPY = xcopy /e
    TRUE = (exit 0)
}
else {
    COPY = cp
    TRUE = true
}

INCLUDEPATH += build

OBJECTS_DIR = build
MOC_DIR = build
RCC_DIR = build
UI_DIR = build
DESTDIR = ../../lib
