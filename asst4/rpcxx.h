// -*- c++ -*-
#ifndef RPCXX_SAMPLE_H
#define RPCXX_SAMPLE_H

#include <iostream>
#include <typeinfo>
#include <cstdlib>
#include "rpc.h"

namespace rpc {

// Protocol is used for encode and decode a type to/from the network.
//
// You may use network byte order, but it's optional. We won't test your code
// on two different architectures.

// TASK1: add more specializations to Protocol template class to support more
// types.
template <typename T> struct Protocol {
  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const T &x) {
    return false;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, T &x) {
    return false;
  }
};

template <> struct Protocol<int> {
  static constexpr size_t TYPE_SIZE = sizeof(int);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const int &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, int &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};


//void
template <> struct Protocol<void> {

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len) {
    *out_len = 0;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok) {
    *in_len = 0;
    return true;
  }
};

// bool
template <> struct Protocol<bool> {
  static constexpr size_t TYPE_SIZE = sizeof(bool);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const bool &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, bool &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// char
template <> struct Protocol<char> {
  static constexpr size_t TYPE_SIZE = sizeof(char);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const char &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, char &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// short
template <> struct Protocol<short> {
  static constexpr size_t TYPE_SIZE = sizeof(short);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const short &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, short &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// long
template <> struct Protocol<long> {
  static constexpr size_t TYPE_SIZE = sizeof(long);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const long &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, long &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// long long
template <> struct Protocol<long long> {
  static constexpr size_t TYPE_SIZE = sizeof(long long);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const long long &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, long long &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// float
template <> struct Protocol<float> {
  static constexpr size_t TYPE_SIZE = sizeof(float);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const float &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, float &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// double
template <> struct Protocol<double> {
  static constexpr size_t TYPE_SIZE = sizeof(double);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const double &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, double &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// std::string
template <> struct Protocol<std::string> {

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const std::string &x) {
    int STR_SIZE;

    if (x.length() % 4 == 0) {
      STR_SIZE = x.length();
    }
    else {
      STR_SIZE = x.length() + (4 - x.length() % 4);
    }

    if (*out_len < sizeof(int) + size_t(STR_SIZE)) return false;

    std::string encoded_string (x);

    for (int i = 0; i < int(STR_SIZE - x.length()); i++) {
      encoded_string.append("\0");
    }

    memcpy(out_bytes, &STR_SIZE, sizeof(int));
    memcpy(out_bytes + sizeof(int), encoded_string.data(), size_t(STR_SIZE));
    *out_len = sizeof(int) + size_t(STR_SIZE);
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, std::string &x) {
    if (*in_len < sizeof(int)) {
      return false;
    }

    int STR_SIZE;
    memcpy(&STR_SIZE, in_bytes, sizeof(int));
    
    if (*in_len < sizeof(int) + size_t(STR_SIZE)) return false;

    // empty string case
    if (STR_SIZE == 0) {
      x.clear();
      *in_len = sizeof(int);
      return true;
    }

    char* decoded_string = new char[STR_SIZE];

    memcpy(decoded_string, in_bytes + sizeof(int), size_t(STR_SIZE));

    x.clear();

    for (int i = 0; i < STR_SIZE; i++) {
      x.push_back(decoded_string[i]);
    }

    size_t pos = x.find('\0');

    if (pos != std::string::npos) {
      x.erase(pos);
    }

    delete[] decoded_string;

    *in_len = sizeof(int) + size_t(STR_SIZE);
    return true;
  }
};

// unsigned int
template <> struct Protocol<unsigned int> {
  static constexpr size_t TYPE_SIZE = sizeof(unsigned int);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const unsigned int &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, unsigned int &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// unsigned char
template <> struct Protocol<unsigned char> {
  static constexpr size_t TYPE_SIZE = sizeof(unsigned char);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const unsigned char &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, unsigned char &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// unsigned short
template <> struct Protocol<unsigned short> {
  static constexpr size_t TYPE_SIZE = sizeof(unsigned short);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const unsigned short &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, unsigned short &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// unsigned long
template <> struct Protocol<unsigned long> {
  static constexpr size_t TYPE_SIZE = sizeof(unsigned long);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const unsigned long &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, unsigned long &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};

// unsigned long long
template <> struct Protocol<unsigned long long> {
  static constexpr size_t TYPE_SIZE = sizeof(unsigned long long);

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const unsigned long long &x) {
    if (*out_len < TYPE_SIZE) return false;
    memcpy(out_bytes, &x, TYPE_SIZE);
    *out_len = TYPE_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, unsigned long long &x) {
    if (*in_len < TYPE_SIZE) return false;
    memcpy(&x, in_bytes, TYPE_SIZE);
    *in_len = TYPE_SIZE;
    return true;
  }
};



// TASK2: Client-side--------------------------------------------------------------------
 
class NoParam: public BaseParams {
  public:
    bool Encode(uint8_t *out_bytes, uint32_t *out_len) const override {
      *out_len = 0;
      return true;
  }
} ;

template<typename T>
class OneParam : public BaseParams {
  T p;
 public:
  OneParam(T p) : p(p) {}

  bool Encode(uint8_t *out_bytes, uint32_t *out_len) const override {
    if(!Protocol<T>::Encode(out_bytes, out_len, p)) {
        return false;
    }
    return true;
  }
};

template<typename T1, typename T2>
class TwoParam : public BaseParams {
  T1 p;
  T2 q;
 public:
  TwoParam(T1 x, T2 y)  { p = x; q = y;}

  bool Encode(uint8_t *out_bytes, uint32_t *out_len) const override {
        
        auto len = *out_len;

        if(!Protocol<T2>::Encode(out_bytes, &len, q)) return false;
        
        auto next = *out_len - len;
        
        if(!Protocol<T1>::Encode(out_bytes + len, &next, p)) return false;
        
        *out_len = len + next;
        
        std::cout << "Two Param encoded:   \n";
        std::cout << "p = " << p << "\n";
        std::cout << "q = " << q << "\n";
        return true;
  }
};



// TASK2: Server-side

// T1 (Svc::*)(T2) procedure
template <typename Svc, typename T1, typename T2>
class OneProcedure : public BaseProcedure {
  bool DecodeAndExecute(uint8_t *in_bytes, uint32_t *in_len,
                        uint8_t *out_bytes, uint32_t *out_len,
                        bool *ok) override final {
                            
    T2 x;
    if (!Protocol<T2>::Decode(in_bytes, in_len, ok, x) || !*ok) {
      return false;
    }

    using FunctionPointerType = T1 (Svc::*)(T2);
    auto p = func_ptr.To<FunctionPointerType>();
    T1 result = (((Svc *) instance)->*p)(x);
    if (!Protocol<T1>::Encode(out_bytes, out_len, result)) {
      *ok = false;
      return false;
    }
    
    return true;
  }
};

// T1 (Svc::*)(T2,T3) procedure
template <typename Svc, typename T1, typename T2, typename T3>
class TwoProcedure : public BaseProcedure {
  bool DecodeAndExecute(uint8_t *in_bytes, uint32_t *in_len,
                        uint8_t *out_bytes, uint32_t *out_len,
                        bool *ok) override final {
                            
    std::cout << "T1 (Svc::*)(T2,T3) procedure \n";
    
    T2 x;
    T3 y;
    
    auto len = *in_len;

    if (!Protocol<T3>::Decode(in_bytes, &len, ok, y) || !*ok) {
      return false;
    }
    
    auto next = *in_len - len;

    if (!Protocol<T2>::Decode(in_bytes + len, &next, ok, x) || !*ok) {
      return false;
    }
    
    *in_len = next + len;
    
    std::cout << "x = " << x << "\n";
    std::cout << "y = " << y << "\n";
    
    using FunctionPointerType = T1 (Svc::*)(T2,T3);
    auto p = func_ptr.To<FunctionPointerType>();
    T1 result = (((Svc *) instance)->*p)(x,y);
    if (!Protocol<T1>::Encode(out_bytes, out_len, result)) {
      *ok = false;
      return false;
    }
    
    std::cout << "Two Param procedule: encoding done \n";
    
    return true;
  }
};

//T1 (Svc::*)() procedure
template <typename Svc, typename T1>
class NoParamProcedure : public BaseProcedure {
  bool DecodeAndExecute(uint8_t *in_bytes, uint32_t *in_len,
                        uint8_t *out_bytes, uint32_t *out_len,
                        bool *ok) override final {
    
    if (!Protocol<void>::Decode(in_bytes, in_len, ok) || !*ok) {
      return false;
    }

    using FunctionPointerType = T1 (Svc::*)();
    auto p = func_ptr.To<FunctionPointerType>();
    T1 result = (((Svc *) instance)->*p)();
    if (!Protocol<T1>::Encode(out_bytes, out_len, result)) {
      *ok = false;
      return false;
    }
    return true;
  }
};

//void procedure for void Svc* ()
template <typename Svc>
class VoidProcedure : public BaseProcedure {
  bool DecodeAndExecute(uint8_t *in_bytes, uint32_t *in_len,
                        uint8_t *out_bytes, uint32_t *out_len,
                        bool *ok) override final {
                                            
    if (!Protocol<void>::Decode(in_bytes, in_len, ok) || !*ok) {
      return false;
    }

    using FunctionPointerType = void (Svc::*)();
    auto p = func_ptr.To<FunctionPointerType>();
    (((Svc *) instance)->*p)();
    if (!Protocol<void>::Encode(out_bytes, out_len)) {
      *ok = false;
      return false;
    }
    return true;
  }
};

//void procedure for void Svc* (T2,T3)
template <typename Svc, typename T2, typename T3>
class VoidProcedure2 : public BaseProcedure {
  bool DecodeAndExecute(uint8_t *in_bytes, uint32_t *in_len,
                        uint8_t *out_bytes, uint32_t *out_len,
                        bool *ok) override final {
                            
    std::cout << "VoidProcedure2: void Svc* (T2,T3) \n";
                                            
    T2 x;
    T3 y;
    
    auto len = *in_len;

    if (!Protocol<T3>::Decode(in_bytes, &len, ok, y) || !*ok) {
      return false;
    }
    
    auto next = *in_len - len;

    if (!Protocol<T2>::Decode(in_bytes + len, &next, ok, x) || !*ok) {
      return false;
    }
    
    *in_len = next + len;
    
    std::cout << "x = " << x << "\n";
    std::cout << "y = " << y << "\n";
    
    using FunctionPointerType = void (Svc::*)(T2,T3);
    auto p = func_ptr.To<FunctionPointerType>();
    (((Svc *) instance)->*p)(x,y);
    if (!Protocol<void>::Encode(out_bytes, out_len)) {
      *ok = false;
      return false;
    }
    
    return true;
  }
};


 
// TASK2: Client-side

template<typename T>
class Result: public BaseResult {
  T r;
 public:
  bool HandleResponse(uint8_t *in_bytes, uint32_t *in_len, bool *ok)  {
    return Protocol<T>::Decode(in_bytes, in_len, ok, r);
  }

  T &data() { return r; }
};

//void result
template<>
class Result<void> : public BaseResult {
public:
  bool HandleResponse(uint8_t *in_bytes, uint32_t *in_len, bool *ok)  {
    *in_len = 0;
    return true;
  }
};
 



// TASK2: Client-side
class Client : public BaseClient {
    public:
  
  // no parameter call
  template<typename Svc, typename T1> 
  Result<T1> * Call(Svc *svc, T1 (Svc::*func)()) {
    
    int instance_id = svc->instance_id();
    int func_id = svc->LookupExportFunction(MemberFunctionPtr::From(func));
          
    auto result = new Result<T1>();
    if (!Send(instance_id, func_id, new NoParam(), result)) {
      delete result;
      return nullptr;
    }
    return result;
  }
   
  
  //T1 (Svc::)(T2) call
  template <typename Svc, typename T1, typename T2>
  Result<T1> *Call(Svc *svc, T1 (Svc::*func)(T2), T2 x) {
    int instance_id = svc->instance_id();
    int func_id = svc->LookupExportFunction(MemberFunctionPtr::From(func));

    auto result = new Result<T1>();
    if (!Send(instance_id, func_id, new OneParam<T2>(x), result)) {
      delete result;
      return nullptr;
    }
    return result;
  }
  
  //T1 (Svc::)(T2,T3) call (includes T1=void)
  template <typename Svc, typename T1, typename T2, typename T3>
  Result<T1> *Call(Svc *svc, T1 (Svc::*func)(T2,T3), T2 x, T3 y) {
      std::cout << "T1 (Svc::)(T2,T3) call\n";
    int instance_id = svc->instance_id();
    int func_id = svc->LookupExportFunction(MemberFunctionPtr::From(func));

    auto result = new Result<T1>();

    if (!Send(instance_id, func_id, new TwoParam<T2,T3>(x,y), result)) {
      delete result;
      return nullptr;
    }
    return result;
  }
  
  //variadic call
  template<typename Svc, typename T1, typename ...Args> 
  Result<T1> * Call(Svc *svc, T1 (Svc::*func)(Args...), Args...args) {
    
    return nullptr;
  }
   
   
};

// TASK2: Server-side
template <typename Svc>
class Service : public BaseService {
  protected:
  
  //void (Svc::*func)()
  void Export(void (Svc::*func)()) {
    ExportRaw(MemberFunctionPtr::From(func), new VoidProcedure<Svc>());
  }
  
  //void (Svc::*func)(T2,T3)
  template <typename T2, typename T3>
  void Export(void (Svc::*func)(T2,T3)) {
    ExportRaw(MemberFunctionPtr::From(func), new VoidProcedure2<Svc,T2,T3>());
  }
  
  //T1 (Svc::*func)()
  template <typename T1>
  void Export(T1 (Svc::*func)()) {
    ExportRaw(MemberFunctionPtr::From(func), new NoParamProcedure<Svc,T1>());
  }
  
  //T1 (Svc::*func)(T2)
  template <typename T1, typename T2>
  void Export(T1 (Svc::*func)(T2)) {
   ExportRaw(MemberFunctionPtr::From(func), new OneProcedure<Svc,T1,T2>());
  }
  
  //T1 (Svc::*func)(T2,T3)
  template <typename T1, typename T2, typename T3>
  void Export(T1 (Svc::*func)(T2, T3)) {
   ExportRaw(MemberFunctionPtr::From(func), new TwoProcedure<Svc,T1,T2,T3>());
  }
  
};

}

#endif /* RPCXX_SAMPLE_H */
