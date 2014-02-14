#!/usr/bin/awk -f

# Copyright (C) 2014 University Radio York
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Formats roles in a pretty, human-readable way.

BEGIN {
    FS = ":";
}
{
    if ($4 == "h") {
        STATUS = "historic";
    } else if ($4 == "c") {
        STATUS = "current";
    } else {
        STATUS = "unknown";
    }

    if ($5 == "h") {
        TYPE = "head of team";
    } else if ($5 == "a") {
        TYPE = "assistant head of team";
    } else if ($5 == "o") {
        TYPE = "officer";
    } else if ($5 == "m") {
        TYPE = "team member";
    } else {
        TYPE = "unknown";
    }

    print $2
    if ($3 != "") {
        print "- Description: " $3
    }
    if ($1 != "") {
        print "- Email Alias: " $1
    }
    print "- Status:      " STATUS
    print "- Type:        " TYPE
    print ""
}
