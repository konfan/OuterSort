#ifndef V8WRAPPER_H__ 
#define V8WRAPPER_H__ 
#include <string.h>
#include <stdlib.h>
#include <jni.h>
#include <v8.h>
#include <utils/Log.h>
#ifdef LOG_TAG
#undef LOG_TAG
#endif
#define LOG_TAG "v8test"

#ifdef __cplusplus
extern "C"
{
    void Java_com_v8test_V8testActivity_registroot(JNIEnv *env,jobject jobj);
}
#endif

class RootLayout
{
private:
    jobject _root;
public:
    RootLayout():_root(NULL){}
    void Init(JNIEnv *env,jobject obj);
};

class GlobalVariable
{
private:
    static GlobalVariable * _inst;
    bool jniinited;
    bool v8inited;
    v8::Persistent<v8::Context> g_context;
    GlobalVariable():jniinited(false),jvm(0),root(0),v8inited(false)
    {}
public:
    static GlobalVariable * GetV();
    bool JniInitialed(){return jniinited;}
    bool V8Initialed(){return v8inited;}
    void InitJni(JNIEnv * env,jobject jobj);
    void InitV8();
    JavaVM * jvm;
    RootLayout * root;
};

class Button
{
};

static void call_setc(JNIEnv *env, jobject thiz);
static char * js_buf = NULL;
static char * g_textbuf = NULL;

//v8 functions
//getapp: set a GetApp() function
static v8::Handle<v8::Object> getapp(const v8::Arguments &args);

//make root template
static v8::Handle<v8::Object> MakeRootTemplate();

//make button template
static v8::Handle<v8::Object> MakeButtonTemplate();
#endif
