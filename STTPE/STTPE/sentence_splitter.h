/* Korean Sentence Splitter
 * Split Korean text into sentences using heuristic algorithm.
 *
 * Copyright (C) 2019 Sang-Kil Park <skpark1224@hyundai.com>
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the BSD license.  See the LICENSE file for details.
 */
#ifndef __SENTENCE_SPLITTER_H
#define __SENTENCE_SPLITTER_H

#include <string>
#include <iostream>
#include <vector>
#include <unordered_map>

#include <algorithm>
#include <cctype>
#include <stack>

#define DEBUG false

namespace kss {
    enum Stats {
        DEFAULT = 0,
        DA      = 1,
        YO      = 2,
        SB      = 3,
        COMMON  = 4,
    };

    enum ID {
        NONE    = 0,        // 0x00
        PREV    = 1 << 0,   // 0x01
        CONT    = 1 << 1,   // 0x02
        NEXT    = 1 << 2,   // 0x04
        NEXT1   = 1 << 3,   // 0x08
        NEXT2   = 1 << 4,   // 0x16
    };

    // Pattern Mapping Table for Sentence Splitter.
    static std::unordered_map<int, std::unordered_map<std::string, int>>
        map ({
            {Stats::DA, {
                {"갔", ID::PREV}, {"간", ID::PREV}, {"겠", ID::PREV}, {"겼", ID::PREV},
                {"같", ID::PREV},

                {"놨", ID::PREV}, {"녔", ID::PREV}, {"니", ID::PREV}, {"낸", ID::PREV},
                {"냈", ID::PREV},

                {"뒀", ID::PREV}, {"때", ID::PREV},

                {"랐", ID::PREV}, {"럽", ID::PREV}, {"렵", ID::PREV}, {"렸", ID::PREV},
                {"린", ID::PREV}, {"뤘", ID::PREV},

                {"밌", ID::PREV},

                {"봤", ID::PREV},

                {"서", ID::PREV}, {"섰", ID::PREV}, {"샜", ID::PREV},

                {"않", ID::PREV}, {"았", ID::PREV}, {"없", ID::PREV}, {"었", ID::PREV},
                {"였", ID::PREV}, {"온", ID::PREV}, {"웠", ID::PREV}, {"이", ID::PREV},
                {"인", ID::PREV}, {"있", ID::PREV},

                {"졌", ID::PREV},

                {"쳤", ID::PREV}, {"챘", ID::PREV},

                {"팠", ID::PREV}, {"펐", ID::PREV},

                {"했", ID::PREV}, {"혔", ID::PREV},

                {"가", ID::NEXT},
                {"고", ID::NEXT | ID::NEXT2},
                {"는", ID::NEXT | ID::NEXT2},
                {"라", ID::NEXT},
                {"를", ID::NEXT},
                {"만", ID::NEXT},
                {"며", ID::NEXT | ID::NEXT2},
                {"면", ID::NEXT | ID::NEXT1 | ID::NEXT2},
                {"서", ID::PREV | ID::NEXT2},
                {"싶", ID::PREV | ID::NEXT},
                {"죠", ID::NEXT},
                {"죵", ID::NEXT},
                {"쥬", ID::NEXT},
                {"하", ID::PREV | ID::NEXT1},
                {"해", ID::NEXT1},
                {"도", ID::NEXT2},
            }},
            {Stats::YO, {
                {"가", ID::PREV}, {"구", ID::PREV}, {"군", ID::PREV}, {"걸", ID::PREV},
                {"까", ID::PREV}, {"께", ID::PREV}, {"껴", ID::PREV},

                {"네", ID::PREV}, {"나", ID::PREV},

                {"데", ID::PREV}, {"든", ID::PREV},

                {"서", ID::PREV}, {"세", ID::PREV},

                {"아", ID::PREV}, {"어", ID::PREV}, {"워", ID::PREV}, {"에", ID::PREV},
                {"예", ID::PREV}, {"을", ID::PREV},

                {"져", ID::PREV}, {"줘", ID::PREV}, {"지", ID::PREV},

                {"춰", ID::PREV},

                {"해", ID::PREV},

                {"고", ID::PREV | ID::NEXT2},
                {"는", ID::NEXT},
                {"라", ID::NEXT1},
                {"를", ID::NEXT},
                {"며", ID::NEXT2},
                {"면", ID::PREV | ID::NEXT2},
                {"하", ID::NEXT1},
            }},
            {Stats::SB, {
                {"가", ID::PREV}, {"까", ID::PREV}, {"거", ID::PREV}, {"걸", ID::PREV},
                {"껄", ID::PREV},

                {"나", ID::PREV}, {"니", ID::PREV},

                {"다", ID::PREV}, {"도", ID::PREV}, {"든", ID::PREV},

                {"랴", ID::PREV}, {"래", ID::PREV},

                {"마", ID::PREV},

                {"봐", ID::PREV},

                {"서", ID::PREV},

                {"아", ID::PREV}, {"어", ID::PREV}, {"오", ID::PREV}, {"요", ID::PREV},
                {"을", ID::PREV},

                {"자", ID::PREV}, {"지", ID::PREV}, {"죠", ID::PREV},

                {"고", ID::PREV | ID::NEXT2},
                {"는", ID::NEXT},
                {"라", ID::PREV | ID::NEXT},
                {"며", ID::NEXT2},
                {"면", ID::NEXT2},
                {"하", ID::NEXT1},
            }},
            {Stats::COMMON, {
                {"ㅋ", ID::CONT}, {"ㅅ", ID::CONT}, {"ㅎ", ID::CONT}, {"ㅠ", ID::CONT},
                {"ㅜ", ID::CONT}, {"^", ID::CONT}, {";", ID::CONT}, {".", ID::CONT},
                {"?", ID::CONT}, {"!", ID::CONT}, {")", ID::CONT}, {"~", ID::CONT},
                {"…", ID::CONT}, {",", ID::CONT},
            }},
        });

    int getUTF8ChrLength(const std::string &text, size_t i);

    constexpr unsigned int str2hash(const char *str, int h);

    void ltrim(std::string &s);
    void rtrim(std::string &s);
    void trim(std::string &s);

    void doTrimSentPushResults(std::string &curSentence, std::vector<std::string> &results);
    void doPushPopSymbol(std::stack<std::string> &stack, const std::string &symbol);
}

std::vector<std::string> splitSentences(const std::string &text);

#endif // __SENTENCE_SPLITTER_H
