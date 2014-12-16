win32 {
    COPY = robocopy /s /e /y
    MKDIR = mkdir
}
else {
    COPY = cp -r
    MKDIR = mkdir -p
}

TEMPLATE = lib
CONFIG += staticlib

OBJECTS_DIR = build
MOC_DIR = build
RCC_DIR = build
UI_DIR = build
DESTDIR = ../../lib
