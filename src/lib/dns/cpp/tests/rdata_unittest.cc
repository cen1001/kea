// Copyright (C) 2010  Internet Systems Consortium, Inc. ("ISC")
//
// Permission to use, copy, modify, and/or distribute this software for any
// purpose with or without fee is hereby granted, provided that the above
// copyright notice and this permission notice appear in all copies.
//
// THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH
// REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
// AND FITNESS.  IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT,
// INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
// LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
// OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
// PERFORMANCE OF THIS SOFTWARE.

// $Id: rrtype_unittest.cc 476 2010-01-19 00:29:28Z jinmei $

#include <vector>

#include <dns/buffer.h>
#include <dns/messagerenderer.h>
#include <dns/rdata.h>
#include <dns/rdataclass.h>
#include <dns/rrclass.h>
#include <dns/rrtype.h>

#include <gtest/gtest.h>

#include "unittest_util.h"
#include "rdata_unittest.h"

using isc::UnitTestUtil;
using namespace std;
using namespace isc::dns;
using namespace isc::dns::rdata;

namespace isc {
namespace dns {
namespace rdata {
RdataTest::RdataTest() :
    obuffer(0), renderer(obuffer),
    rdata_nomatch(createRdata(RRType(0), RRClass(1), "\\# 0"))
{}

RdataPtr
RdataTest::rdataFactoryFromFile(const RRType& rrtype, const RRClass& rrclass,
                                const char* datafile, size_t position)
{
    std::vector<unsigned char> data;
    UnitTestUtil::readWireData(datafile, data);

    InputBuffer buffer(&data[0], data.size());
    buffer.setPosition(position);

    uint16_t rdlen = buffer.readUint16();
    return (createRdata(rrtype, rrclass, buffer, rdlen));
}
}
}
}
