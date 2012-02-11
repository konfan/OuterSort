#ifndef _V8_DEMO_H__ 
#define _V8_DEMO_H__ 
#include <string.h>
#include <stdlib.h>
#include <jni.h>
#include <v8.h>
#include <utils/Log.h>
#include <memory>
#ifdef LOG_TAG
#undef LOG_TAG
#endif
#define LOG_TAG "V8Cpp"

#ifdef __cplusplus
extern "C"
{
    jboolean Java_com_v8demo_V8demoActivity_initclass(JNIEnv *env,jobject jobj);
}
#endif

class v8helper
{
public:
    static v8helper * GetInstance();
private:
    static v8helper * _val;
    v8::HandleScope m_handle_scope;
    v8::Persistent<v8::Context> m_context;
    v8::Handle<v8::ObjectTemplate> m_templ;
private:
    void RegistUserDefine();
    v8helper();
    ~v8helper();
    v8helper(const v8helper &);
    v8helper & operator=(const v8helper &);
};

class RootView
{
public:
}
#endif
