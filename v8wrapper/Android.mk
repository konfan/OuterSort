# 
# Copyright 2006 The Android Open Source Project
#
# Android Asset Packaging Tool
#

ifneq ($(TARGET_SIMULATOR),true)

LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)

LOCAL_SRC_FILES := v8wrapper.cpp

LOCAL_C_INCLUDES += $(LOCAL_PATH)/../../webkit/WebKit/android/JavaVM \
	$(LOCAL_PATH)/lib \
	$(LOCAL_PATH)/../../v8/include

LOCAL_CFLAGS +=-O0
LOCAL_MODULE := libv8wrapper
LOCAL_SHARED_LIBRARIES := libcutils
LOCAL_STATIC_LIBRARIES := libv8
LOCAL_PRELINK_MODULE := false
include $(BUILD_SHARED_LIBRARY)

endif # TARGET_SIMULATOR != true
