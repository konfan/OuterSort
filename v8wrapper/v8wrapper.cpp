#include "v8wrapper.h"

void Java_com_v8test_V8testActivity_registroot(JNIEnv *env,jobject jobj)
{
    GlobalVariable * gl = GlobalVariable::GetV();
    if( ! gl->JniInitialed())
        gl->InitJni(env,jobj);
    gl->root = new RootLayout();
    gl->root->Init(env,jobj);
}

GlobalVariable * GlobalVariable::_inst = 0;
GlobalVariable * GlobalVariable::GetV()
{
    if(!_inst)
        _inst = new GlobalVariable();
    return _inst;
}

void GlobalVariable::InitJni(JNIEnv * env,jobject jobj)
{
    env->GetJavaVM( & jvm);
    if( jvm)
        jniinited = true;
}

void GlobalVariable::InitV8()
{
    v8::HandleScope handle_scope;
    //create built-in functions
    g_context = v8::Context::New();
    v8::ContextScope context_scope(g_context);
    g_context->Global()->k
}
v8::Handle<v8::Object> MakeRootTemplate()
{
    v8::HandleScope handle_scope;
    v8::Handle<v8::ObjectTemplate> result = v8::ObjectTemplate::New();
    result->Set(v8::String::New("GetApp"),v8::FunctionTemplate::New(getapp));
    v8::Handle<v8::FunctionTemplate> vf_getroot = v8::FunctionTemplate::New();
}




void RootLayout::Init(JNIEnv *env,jobject obj)
{
    jclass jc = env->GetObjectClass(obj);
    jfieldID jfid = env->GetFieldID(jc,"root","Landroid/widget/LinearLayout");
    jobject localroot= env->GetObjectField(obj,jfid);
    _root = env->NewGlobalRef(localroot);
}

