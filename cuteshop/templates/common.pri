

win32 {
    COPY = xcopy /e /q
    MKDIR = mkdir
    TRUE = (exit 0)
}
else {
    COPY = cp
    MKDIR = mkdir -p
    TRUE = true
}

INCLUDEPATH += build

OBJECTS_DIR = build
MOC_DIR = build
RCC_DIR = build
UI_DIR = build
DESTDIR = ../../lib
