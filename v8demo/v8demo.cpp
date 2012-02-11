#include "v8demo.h"

static v8::Handel<v8::Value> getroot(const v8::Arguments &args);

jboolean Java_com_v8demo_V8demoActivity_initclass(JNIEnv *env,jobject jobj)
{
    LOGI("init");
    jboolean ret = 1;
    return ret;
}

v8helper::v8helper()
{
    m_templ= v8::ObjectTemplate::New();
    RegistUserDefine();
    m_context = v8::Context::New(NULL,m_templ);
}

v8helper * v8helper::_val = NULL;
v8helper * v8helper::GetInstance()
{
    if(!_val)
        _val = new v8helper();
    return _val;
}

void v8helper::RegistUserDefine()
{
    m_templ->Set(v8::String::New("GetRoot"),v8::FunctionTemplate::New( getroot));
    Handle<FunctionTemplate> root_templ= FunctionTemplate::New();

}
static v8::Handel<v8::Value> getroot(const v8::Arguments &args)
{
    //jni code ,get root
    return v8::Undefined();
}
