win32 {
    MKDIR = mkdir
    COPY = xcopy /e
}
else {
    MKDIR = mkdir -p
    COPY = cp
}

INCLUDEPATH += build

OBJECTS_DIR = build
MOC_DIR = build
RCC_DIR = build
UI_DIR = build
DESTDIR = ../../lib
