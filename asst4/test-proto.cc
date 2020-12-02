#include <gtest/gtest.h>
#include "rpcxx.h"

namespace {

class ProtocolTest : public testing::Test {
 protected:
  uint8_t *buf;
  void SetUp() override {
    buf = new uint8_t[256];
  }

  void TearDown() override {
    delete [] buf;
  }
};

TEST_F(ProtocolTest, UnalignedTest)
{
  double x = 3.14159265358979323846;
  double y = 0.0;
  bool ok = true;
  auto p = buf + 1;
  uint32_t len = 255;

  EXPECT_EQ(true, rpc::Protocol<double>::Encode(p, &len, x));
  EXPECT_EQ(true, rpc::Protocol<double>::Decode(p, &len, &ok, y));

  ASSERT_EQ(ok, true);
  ASSERT_EQ(y, x);
}

TEST_F(ProtocolTest, LongTest)
{
  auto k = std::array<long, 3>({std::numeric_limits<long>::min(), -1, std::numeric_limits<long>::max()});
  for (long x: k) {
    long y = 0xdeadbeefc011fefe;
    uint32_t len = 256;
    bool ok = true;
    EXPECT_EQ(true, rpc::Protocol<long>::Encode(buf, &len, x));
    EXPECT_EQ(true, rpc::Protocol<long>::Decode(buf, &len, &ok, y));

    ASSERT_EQ(ok, true);
    ASSERT_EQ(y, x);
  }
}

TEST_F(ProtocolTest, StringTest)
{
  std::string x = "Four Seasons Landscaping is next to Fantasy Island!";
  std::string y = "";
  uint32_t len = 256;
  bool ok = true;
  EXPECT_EQ(true, rpc::Protocol<std::string>::Encode(buf, &len, x));
  EXPECT_EQ(true, rpc::Protocol<std::string>::Decode(buf, &len, &ok, y));

  ASSERT_EQ(ok, true);
  ASSERT_EQ(x, y);

  len--;
  EXPECT_EQ(false, rpc::Protocol<std::string>::Decode(buf, &len, &ok, y));
  ASSERT_EQ(ok, true);
}

TEST_F(ProtocolTest, EmptyStringTest)
{
  uint32_t len = 256;
  bool ok = true;
  EXPECT_EQ(true, rpc::Protocol<std::string>::Encode(buf, &len, std::string("")));

  std::string x("BIGWIN");
  EXPECT_EQ(true, rpc::Protocol<std::string>::Decode(buf, &len, &ok, x));
  EXPECT_EQ(x, "");
}

}
