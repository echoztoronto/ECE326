// -*- c++ -*-
#ifndef RPCXX_SAMPLE_H
#define RPCXX_SAMPLE_H

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
  static size_t STR_SIZE;

  static bool Encode(uint8_t *out_bytes, uint32_t *out_len, const std::string &x) {

    if (x.length() % 4 == 0) {
      STR_SIZE = x.length();
    }
    else {
      STR_SIZE = x.length() + (4 - x.length() % 4);
    }

    std::string encoded_string (x);

    for (int i = 0; i < int(STR_SIZE - x.length()); i++) {
      encoded_string.append("\0");
    }

    if (*out_len < STR_SIZE) return false;
    memcpy(out_bytes, &encoded_string, STR_SIZE);
    *out_len = STR_SIZE;
    return true;
  }
  static bool Decode(uint8_t *in_bytes, uint32_t *in_len, bool *ok, std::string &x) {
    if (*in_len < STR_SIZE) return false;
    memcpy(&x, in_bytes, STR_SIZE);

    size_t pos = x.find("\0");

    if (pos != std::string::npos) {
      x.erase(pos);
    }

    *in_len = STR_SIZE;
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


// TASK2: Client-side
class IntParam : public BaseParams {
  int p;
 public:
  IntParam(int p) : p(p) {}

  bool Encode(uint8_t *out_bytes, uint32_t *out_len) const override {
    return Protocol<int>::Encode(out_bytes, out_len, p);
  }
};

// TASK2: Server-side
template <typename Svc>
class IntIntProcedure : public BaseProcedure {
  bool DecodeAndExecute(uint8_t *in_bytes, uint32_t *in_len,
                        uint8_t *out_bytes, uint32_t *out_len,
                        bool *ok) override final {
    int x;
    // This function is similar to Decode. We need to return false if buffer
    // isn't large enough, or fatal error happens during parsing.
    if (!Protocol<int>::Decode(in_bytes, in_len, ok, x) || !*ok) {
      return false;
    }
    // Now we cast the function pointer func_ptr to its original type.
    //
    // This incomplete solution only works for this type of member functions.
    using FunctionPointerType = int (Svc::*)(int);
    auto p = func_ptr.To<FunctionPointerType>();
    int result = (((Svc *) instance)->*p)(x);
    if (!Protocol<int>::Encode(out_bytes, out_len, result)) {
      // out_len should always be large enough so this branch shouldn't be
      // taken. However just in case, we return an fatal error by setting *ok
      // to false.
      *ok = false;
      return false;
    }
    return true;
  }
};

// TASK2: Client-side
class IntResult : public BaseResult {
  int r;
 public:
  bool HandleResponse(uint8_t *in_bytes, uint32_t *in_len, bool *ok) override final {
    return Protocol<int>::Decode(in_bytes, in_len, ok, r);
  }
  int &data() { return r; }
};

// TASK2: Client-side
class Client : public BaseClient {
 public:
  template <typename Svc>
  IntResult *Call(Svc *svc, int (Svc::*func)(int), int x) {
    // Lookup instance and function IDs.
    int instance_id = svc->instance_id();
    int func_id = svc->LookupExportFunction(MemberFunctionPtr::From(func));

    // This incomplete solution only works for this type of member functions.
    // So the result must be an integer.
    auto result = new IntResult();

    // We also send the paramters of the functions. For this incomplete
    // solution, it must be one integer.
    if (!Send(instance_id, func_id, new IntParam(x), result)) {
      // Fail to send, then delete the result and return nullptr.
      delete result;
      return nullptr;
    }
    return result;
  }
};

// TASK2: Server-side
template <typename Svc>
class Service : public BaseService {
 protected:
  void Export(int (Svc::*func)(int)) {
    ExportRaw(MemberFunctionPtr::From(func), new IntIntProcedure<Svc>());
  }
};

}

#endif /* RPCXX_SAMPLE_H */
