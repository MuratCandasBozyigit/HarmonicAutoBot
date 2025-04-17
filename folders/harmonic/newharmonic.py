//@version=4
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © fikira
// This source code is subject to the terms of the Creative Commons Zero v1.0 Universal license
// https://github.com/fikira12/Fibonacci-Retracement-Pivots.git
// Copyright (c) 2019 @fikira

study("[fikira] Harmonic Patterns 2", shorttitle="HaPat 2", max_bars_back=300, overlay=true)

no_wick = input(false, title="'NO WICK' [ON = high/low WITHOUT WICK] [OFF = high/low]")
show_z = input(false, title="Show ZigZag")
nwh = close > open ? close : close < open ? open : high // nwh = no wick (high)
nwl = close > open ? open : close < open ? close : low // nwh = no wick (low)

srch = no_wick ? nwh : high // IF "NO WICK" is ON > take the highest price without wick, else take high (with wick)
srcl = no_wick ? nwl : low  // IF "NO WICK" is ON > take the lowest price without wick, else take low (with wick)

ZZPercent = input(1.5, title="Minimum % Change", type=input.float)

trend = 0
trend := na(trend[1]) ? 1 : trend[1]
LL = 0.0
LL := na(LL[1]) ? srcl : LL[1]
HH = 0.0
HH := na(HH[1]) ? srch : HH[1]

PivotChg = ZZPercent * 0.01
zigzag = float(na)

if trend > 0  // trend is up, look for new swing low
    if srch >= HH  // new higher high detected
        HH := srch
        HH
    else
        if srcl < HH * (1 - PivotChg)
            zigzag :=srch[1]
            trend := -1
            LL := srcl
            LL
else
    // trend is down, look for new swing high
    if srcl <= LL  // new lower low detected
        LL := srcl
        LL
    else
        if srch > LL * (1 + PivotChg)
            zigzag := srcl[1]
            trend := 1
            HH := srch
            HH

oc = 0
oc := change(trend) > 0 ? 1 : change(trend) < 0 ? -1 : nz(oc[1])

css = oc == 1 ? color.red : color.blue

pL = zigzag and oc == 1
pH = zigzag and oc == -1

d = valuewhen(not na(zigzag), zigzag, 0)                                        // when there is a new "Highest" or "Lowest" point > use present value
//plot(d, color=color.red, offset=-1)                                           // Shark: 'c' = b

c = valuewhen(not na(zigzag), zigzag, 1)                                        // when there is a new "Highest" or "Lowest" point > use 1 point back as value
//plot(c, color=color.orange, offset=-1)                                        // Shark: 'b' = c 

b = valuewhen(not na(zigzag), zigzag, 2)                                        // when there is a new "Highest" or "Lowest" point > use 2 points back as value
//plot(b, color=color.yellow, offset=-1)                                        // Shark: 'a' = b 

a = valuewhen(not na(zigzag), zigzag, 3)                                        // when there is a new "Highest" or "Lowest" point > use 3 points back as value
//plot(a, color=color.lime, offset=-1)                                          // Shark: 'x' = a 

x = valuewhen(not na(zigzag), zigzag, 4)                                        // when there is a new "Highest" or "Lowest" point > use 4 points back as value
//plot(x, color=color.aqua, offset=-1)                                          // Shark: '0' = x    


dh = d > c and c < b and b > a
dl = d < c and c > b and b < a
ch = c > b and b < a
cl = c < b and b > a
bh = b > a 
bl = b < a
ah = a > x
al = a < x

// Show ZigZag
plot(show_z ? zigzag : na, linewidth=2, color=css, offset=-1)

// Error margin
marge  = input(0, minval=0, maxval=10, step=1, title="Ratio tolerance 0 - 10 %") / 100
marge1 = 1 - marge
marge2 = 1 + marge

// 'Patterns' Visible?
_pt = input(false, title="-<><><><><><><><[Patterns]><><><><><><><>-")

show_anim = input(true, title="Show Animal Symbols")
show_L = input(true, title="Show Labels")
show_D = input(true, title="Show Drawings")
//abcd = input(true, title="Show 'ABCD'")
crab = input(true, title="Show 🦀'CRAB'")
bat = input(true, title="Show 🦇'BAT'")
batA = input(true, title="Show 🦇'BAT' ALT")
//gartley = input(true, title="Show 'Gartley'")
butterfly = input(true, title="Show 🦋'Butterfly'")
shark = input(true, title="Show 🦈'Shark'")

// Show 'Entry'
_E = input(false, title="-<><><><><><><><[Entry Point]><><><><><><><>-")
show_E = input(true, title="Show Entry Points")

// Show 'Stop Loss' Lines

_sl = input(false, title="-<><><><><><><><[Stop Loss]><><><><><><><>-")
show_SL = input(true, title="Show SL Lines")

// Show 'Take Profit' Lines

_tp = input(false, title="-<><><><><><><><[Take Profit]><><><><><><><>-")
show_TP = input(true, title="Show TP Lines")

//TP1 = input(title="TP level 'ABCD'", defval="0.382", options=["0.236", "0.382", "0.5", "0.618", "0.786", "1", "1.272", "1.618"])  // numbers = minutes, D = Day, W = Week, M = Month
TP2 = input(title="TP level 🦀🦇🦋", defval="0.618", options=["0.236", "0.382", "0.5", "0.618", "0.786", "1", "1.272", "1.618"])  // numbers = minutes, D = Day, W = Week, M = Month
TP3 = input(title="TP level 🦀🦇🦋", defval="1.272", options=["0.236", "0.382", "0.5", "0.618", "0.786", "1", "1.272", "1.618"])  // numbers = minutes, D = Day, W = Week, M = Month

//_0_382 = 0.382
//if TP1 == "0.236"
//    _0_382 := 0.236 
//else
//    if TP1 == "0.382"
//        _0_382 := 0.382
//    else
//        if TP1 == "0.5"
//            _0_382 := 0.5
//        else
//            if TP1 == "0.618"
//                _0_382 := 0.618
//            else
//                if TP1 == "0.786"
//                    _0_382 := 0.786
//                else
//                    if TP1 == "1"
//                        _0_382 := 1
//                    else
//                        if TP1 == "1.272"
//                            _0_382 := 1.272
//                        else
//                            if TP1 == "1.618"
//                                _0_382 := 1.618


_0_618 = 0.618
if TP2 == "0.236"
    _0_618 := 0.236 
else
    if TP2 == "0.382"
        _0_618 := 0.382
    else
        if TP2 == "0.5"
            _0_618 := 0.5
        else
            if TP2 == "0.618"
                _0_618 := 0.618
            else
                if TP2 == "0.786"
                    _0_618 := 0.786
                else
                    if TP2 == "1"
                        _0_618 := 1
                    else
                        if TP2 == "1.272"
                            _0_618 := 1.272
                        else
                            if TP2 == "1.618"
                                _0_618 := 1.618


_1_272 = 1.272
if TP3 == "0.236"
    _1_272 := 0.236 
else
    if TP3 == "0.382"
        _1_272 := 0.382
    else
        if TP3 == "0.5"
            _1_272 := 0.5
        else
            if TP3 == "0.618"
                _1_272 := 0.618
            else
                if TP3 == "0.786"
                    _1_272 := 0.786
                else
                    if TP3 == "1"
                        _1_272 := 1
                    else
                        if TP3 == "1.272"
                            _1_272 := 1.272
                        else
                            if TP3 == "1.618"
                                _1_272 := 1.618


SIZE = input(title="Size Label", defval="tiny", options=["tiny", "small", "normal", "huge"])  


_SIZE = size.small
if SIZE == "tiny"
    _SIZE := size.tiny
else
    if SIZE == "small"
        _SIZE := size.small
    else
        if SIZE == "normal"
            _SIZE := size.normal
        else
            if SIZE == "huge"
                _SIZE := size.huge

  
//tp_0_382 = d + ((a - d) * _0_382) // tp_1 = tp_0_382
tp_0_618 = d + ((a - d) * _0_618) // tp_2 = tp_0_618
tp_0_618a = d + ((c - d) * _0_618)  // tp_1a = tp_0_618a
tp_0_886 = d + ((c - d) * 0.886) 
tp_1_272 = d + ((c - d) * _1_272)  // tp_2a = tp_1_272

//tp0_382 = d - ((d - a) * _0_382) // tp1 = tp0_382
tp0_618 = d - ((d - a) * _0_618) // tp2 = tp0_618
tp0_618a = d - ((d - c) * _0_618) // tp1a = tp0_618a
tp0_886 = d - ((d - c) * 0.886) 
tp1_272 = d - ((d - c) * _1_272)  // tp2a = tp1_272

 


tp_0_5 = d + ((c - d) * 0.5) // tp_1s = tp_0_5
tp0_5 = d - ((d - c) * 0.5) // tp1s = tp0_5

e_0_886 = a - ((a - x) * 0.886) // e_1s = e_0_886
e0_886 = a + ((x - a) * 0.886) // e1s = e0_886


// 'ABCD'

// ABCD Bullish

//c_bl = ch and c >= (b + (((a - b) * 0.618) * marge1)) and c <= (b + (((a - b) * 0.786) * marge2)) 
//d_bl = dl and d >= (c - (((c - b) * 1.618) * marge2)) and d <= (c - (((c - b) * 1.272) * marge1)) 
//ABCD_bl = c_bl and d_bl

// ABCD Bearish

//c_br = cl and c <= (b - (((b - a) * 0.618) * marge1)) and c >= (b - (((b - a) * 0.786) * marge2)) 
//d_br = dh and d <= (c + (((b - c) * 1.618) * marge2)) and d >= (c + (((b - c) * 1.272) * marge1)) 
//ABCD_br = c_br and d_br

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// When the market arrives at a point, where D may be situated, don’t rush into a trade.                                        //
// Use some techniques to make sure that the price reversed up (or down if it’s a bearish ABCD).                                //    
// The best scenario is a reversal candlestick pattern. A buy order may be set at or above the high of the candle at point D.   //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Take Profit Points (TP) ABCD
// Put a Stop Loss in line with your rules of risk management.

//TP_1 = abcd and dl and ABCD_bl ? valuewhen(tp_0_382, tp_0_382, 0) : abcd and dh and ABCD_br ? valuewhen(tp0_382, tp0_382, 0) : na
//TP_2 = abcd and dl and ABCD_bl ? valuewhen(tp_0_618, tp_0_618, 0) : abcd and dh and ABCD_br ? valuewhen(tp0_618, tp0_618, 0) : na
//TP_3 = abcd and dl and ABCD_bl ? a : abcd and dh and ABCD_br ? a : na

// CRAB

// Crab Bullish

cr_b_bl = bl and b <= (a - (((a - x) * 0.382) * marge1)) and b >= (a - (((a - x) * 0.618) * marge2)) 
cr_c_bl = ch and c <= (b + (((a - b) * 0.886) * marge2)) and c >= (b + (((a - b) * 0.382) * marge1)) 
cr_D_bl = dl and d <= (a - (((a - x) * 1.618) * marge1))
cr_d_bl_ = dl and d >= (a - (((a - b) * 2.24) * marge2))
cr_d_bl = dl and d >= (a - (((a - b) * 3.618) * marge2))

//- Point b is at the 38.2-61.8% retracement of xa
//- Point c can be at the 38.2%-88.6% retracement of ab
//- Point d can be found at the 224%-316% extension of ab or at the 161.8% extension of xa 
// The closer d is to the 161.8% extension of x, the stronger is the signal of this pattern

cr_bl = cr_b_bl and cr_c_bl and cr_D_bl and cr_d_bl
plot_cr_bl = cr_bl and not cr_bl[1] ? cr_bl : na
plotchar(crab and show_anim ? plot_cr_bl : na, char="🦀", location=location.bottom, transp=0, size=size.tiny, title="Crab Bullish")
cr_bl_strong = cr_b_bl and cr_c_bl and cr_D_bl and cr_d_bl_
plot_cr_bl_strong = cr_bl_strong and not cr_bl_strong[1] ? cr_bl_strong : na
plotchar(crab and show_anim ? plot_cr_bl_strong : na, char="🦀", location=location.bottom, transp=0, size=size.small, title="Crab Bullish Strong")

// Crab Bearish

cr_b_br = bh and b >= (a + (((x - a) * 0.382) * marge1)) and b <= (a + (((x - a) * 0.618) * marge2)) 
cr_c_br = cl and c >= (b - (((b - a) * 0.886) * marge2)) and c <= (b - (((b - a) * 0.382) * marge1)) 
cr_D_br = dh and d >= (a + (((x - a) * 1.618) * marge1))
cr_d_br_ = dh and d <= (a + (((b - a) * 2.24) * marge2))
cr_d_br = dh and d <= (a + (((b - a) * 3.618) * marge2))

//- Point b is at the 38.2-61.8% retracement of xa
//- Point c can be at the 38.2%-88.6% retracement of ab
//- Point d can be found at the 224%-316% extension of ab or at the 161.8% extension of xa 
// The closer d is to the 161.8% extension of x, the stronger is the signal of this pattern

cr_br = cr_b_br and cr_c_br and cr_D_br and cr_d_br
plot_cr_br = cr_br and not cr_br[1] ? cr_br : na
plotchar(crab and show_anim ? plot_cr_br : na, char="🦀", location=location.top, transp=0, size=size.tiny, title="Crab Bearish")
cr_br_strong = cr_b_br and cr_c_br and cr_D_br and cr_d_br_
plot_cr_br_strong = cr_br_strong and not cr_br_strong[1] ? cr_br_strong : na
plotchar(crab and show_anim ? plot_cr_br_strong : na, char="🦀", location=location.top, transp=0, size=size.small, title="Crab Bearish Strong")

// Take Profit lines Crab

//The entry is at the point d. 
//Always wait for the market to reverse from cd before opening your trade. 
//Take Profit may be at 61.8% (0.618) of cd (TP3), and 127.2% (1.272) of cd (TP4)
// Put a Stop Loss in line with your rules of risk management.

ENTRYcr = dl and cr_bl ? d : dh and cr_br ? d : na

TP_1cr = dl and cr_bl or cr_bl_strong ? valuewhen(tp_0_618a, tp_0_618a, 0) : dh and cr_br or cr_br_strong ? valuewhen(tp0_618a, tp0_618a, 0) : na
TP_2cr = dl and cr_bl or cr_bl_strong ? valuewhen(tp_1_272, tp_1_272, 0) : dh and cr_br or cr_br_strong ? valuewhen(tp1_272, tp1_272, 0) : na

// BAT


// BAT Bullish

bt_b_bl = bl and b <= (a - (((a - x) * 0.382) * marge1)) and b >= (a - (((a - x) * 0.5) * marge2)) 
bt_c_bl = ch and c <= (b + (((a - b) * 0.886) * marge2)) and c >= (b + (((a - b) * 0.382) * marge1)) 
bt_d_bl = dl and d <= (a - (((a - b) * 1.618) * marge2)) and d >= (a - (((a - b) * 2.618) * marge2))

//- Point B is at the 38.2-50% retracement of XA.
//- Point C can be at the 38.2%-88.6% retracement of AB.
//- Point D can be found at the 161.8%-261.8% extension of AB or at the 88.6% retracement of XA.

bt_bl = bt_b_bl and bt_c_bl and bt_d_bl
plot_bt_bl = bt_bl and not bt_bl[1] ? bt_bl : na
plotchar(bat and show_anim ? plot_bt_bl : na, char="🦇", location=location.bottom, transp=0, size=size.small, title="Bat Bullish")

// Bat Bearish

bt_b_br = bh and b >= (a + (((x - a) * 0.382) * marge1)) and b <= (a + (((x - a) * 0.5) * marge2)) 
bt_c_br = cl and c >= (b - (((b - a) * 0.886) * marge2)) and c <= (b - (((b - a) * 0.382) * marge1)) 
bt_d_br = dh and d >= (a + (((b - a) * 1.618) * marge2)) and d <= (a + (((b - a) * 2.618) * marge2))

//- Point B is at the 38.2-50% retracement of XA.
//- Point C can be at the 38.2%-88.6% retracement of AB.
//- Point D can be found at the 161.8%-261.8% extension of AB or at the 88.6% retracement of XA.

bt_br = bt_b_br and bt_c_br and bt_d_br
plot_bt_br = bt_br and not bt_br[1] ? bt_br : na
plotchar(bat and show_anim ? plot_bt_br : na, char="🦇", location=location.top, transp=0, size=size.small, title="Bat Bearish")

// Take Profit lines Bat

//The entry is at the point D. As usual, a confirmation of the market’s reversal here is necessary. 
//Take Profit may be at 61.8% of CD, 127.2% of CD, and/or the projection of XA from D. Put a Stop Loss in line with your rules of risk management.
// Put a Stop Loss in line with your rules of risk management.

ENTRYbt = dl and bt_bl ? d : dh and bt_br ? d : na
TP_1bt = dl and bt_bl ? valuewhen(tp_0_618a, tp_0_618a, 0) : dh and bt_br ? valuewhen(tp0_618a, tp0_618a, 0) : na
TP_2bt = dl and bt_bl ? valuewhen(tp_1_272, tp_1_272, 0) : dh and bt_br ? valuewhen(tp1_272, tp1_272, 0) : na
TP_3bt = dl and bt_bl ? d + (a - x) : dh and bt_br ? d - (x - a) : na

// ALTERNATIVE BAT

// BAT ALT Bullish

bt_b_blA = bl and b >= (a - (((a - x) * 0.39) * marge2))
bt_c_blA = ch and c <= (b + (((a - b) * 0.886) * marge2)) and c >= (b + (((a - b) * 0.382) * marge1))
bt_d1_blA = bl and d <= (a - (((a - x) * 1.11) * marge1)) and d >= (a - (((a - x) * 1.15) * marge2)) 
bt_d2_blA = dl and d <= (c - (((c - b) * 2.0) * marge2)) and d >= (c - (((c - b) * 3.618) * marge2))

bt_blA = bt_b_blA and bt_c_blA and bt_d1_blA and bt_d2_blA
plot_bt_blA = bt_blA and not bt_blA[1] ? bt_blA : na
plotchar(batA and show_anim ? plot_bt_blA : na, char="🦇", text="ALT", textcolor=color.lime, location=location.bottom, transp=0, size=size.small, title="Bat ALT Bullish")

// Bat ALT Bearish

bt_b_brA = bh and b <= (a + (((x - a) * 0.39) * marge2)) 
bt_c_brA = cl and c >= (b - (((b - a) * 0.886) * marge2)) and c <= (b - (((b - a) * 0.382) * marge1)) 
bt_d1_brA = bh and d >= (a + (((x - a) * 1.11) * marge1)) and d <= (a + (((x - a) * 1.15) * marge2)) 
bt_d2_brA = dh and d >= (c + (((b - c) * 2.0) * marge2)) and d <= (c + (((b - c) * 3.618) * marge2))

bt_brA = bt_b_brA and bt_c_brA and bt_d1_brA and bt_d2_brA
plot_bt_brA = bt_brA and not bt_brA[1] ? bt_brA : na
plotchar(batA and show_anim ? plot_bt_brA : na, char="🦇", text="ALT", textcolor=color.red, location=location.top, transp=0, size=size.small, title="Bat ALT Bearish")

// Take Profit lines ALT Bat

//The entry is at the point D. As usual, a confirmation of the market’s reversal here is necessary. 
//Take Profit may be at 61.8% of CD, 88.6% of CD, and/or B & C. Put a Stop Loss in line with your rules of risk management.
// Put a Stop Loss in line with your rules of risk management.

ENTRYbtA = dl and bt_blA ? d : dh and bt_brA ? d : na
TP_1btA = dl and bt_blA ? valuewhen(tp_0_618a, tp_0_618a, 0) : dh and bt_brA ? valuewhen(tp0_618a, tp0_618a, 0) : na
TP_2btA = dl and bt_blA ? valuewhen(tp_0_886, tp_0_886, 0) : dh and bt_brA ? valuewhen(tp0_886, tp0_886, 0) : na
TP_3btA = dl and bt_blA ? b : dh and bt_brA ? b : na
TP_4btA = dl and bt_blA ? c : dh and bt_brA ? c : na


// GARTLEY

// Gartley Bullish

//g_b_bl = bl and b <= (a - (((a - x) * 0.624) * marge1)) and b >= (a - (((a - x) * 0.612) * marge2)) 
//g_c_bl = ch and c <= (b + (((a - b) * 0.886) * marge2)) and c >= (b + (((a - b) * 0.382) * marge1)) 
//g_d_bl = dl and d <= (a - (((a - b) * 1.27) * marge2)) and d >= (a - (((a - b) * 1.618) * marge2))

//Point B is at the 61.8% retracement of XA. This is the most important condition.
//Point C can be at the 38.2%-88.6% retracement of AB.
//Point D can be found at the 127.2%-161.8% extension of AB or at the 78.6% retracement of XA.

//g_bl = g_b_bl and g_c_bl and g_d_bl
//plot_g_bl = g_bl and not g_bl[1] ? g_bl : na

// Gartley Bearish

//g_b_br = bh and b >= (a + (((x - a) * 0.624) * marge1)) and b <= (a + (((x - a) * 0.612) * marge2)) 
//g_c_br = cl and c >= (b - (((b - a) * 0.886) * marge2)) and c <= (b - (((b - a) * 0.382) * marge1)) 
//g_d_br = dh and d >= (a + (((b - a) * 1.27) * marge2)) and d <= (a + (((b - a) * 1.618) * marge2))

//Point B is at the 61.8% retracement of XA. This is the most important condition.
//Point C can be at the 38.2%-88.6% retracement of AB.
//Point D can be found at the 127.2%-161.8% extension of AB or at the 78.6% retracement of XA.

//g_br = g_b_br and g_c_br and g_d_br
//plot_g_br = g_br and not g_br[1] ? g_br : na

// Take Profit lines Gartley

//TP1: 61.8% of CD
//TP2: the size of XA projected from D
//SL1: Stop Loss at x (+/-1%?)
// Put a Stop Loss in line with your rules of risk management.

//ENTRYg = dl and g_bl ? d : dh and g_br ? d : na
//TP_1g = dl and g_bl ? valuewhen(tp_0_618a, tp_0_618a, 0) : dh and g_br ? valuewhen(tp0_618a, tp0_618a, 0) : na
//TP_2g = dl and g_bl ? d + (a - x) : dh and g_br ? d - (x - a) : na
//SL_1g = dl and g_bl ? x - (x / 100) : dh and g_br ? x + (x / 100) : na

// BUTTERFLY

// Butterfly Bullish

b_b_bl = bl and b <= (a - (((a - x) * 0.794) * marge1)) and b >= (a - (((a - x) * 0.778) * marge2)) 
b_c_bl = ch and c <= (b + (((a - b) * 0.886) * marge2)) and c >= (b + (((a - b) * 0.382) * marge1)) 
b_d_bl = dl and d <= (a - (((a - b) * 1.618) * marge2)) and d >= (a - (((a - b) * 2.618) * marge2))

//- Point B is at up to 78.6% retracement of XA.
//- Point C can be at the 38.2%-88.6% retracement of AB.
//- Point D can be found at the 161.8%-261.8% extension of AB or at the 127.2%-161.8% extension of XA. 
// The difference from a Gartley pattern is that D is not at the retracement of XA but at its extension.

b_bl = b_b_bl and b_c_bl and b_d_bl
plot_b_bl = b_bl and not b_bl[1] ? b_bl : na
plotchar(butterfly and show_anim ? plot_b_bl : na, char="🦋", location=location.bottom, color=color.lime, transp=0, size=size.small, title="Butterfly Bullish")

// Butterfly Bearish

b_b_br = bh and b >= (a + (((x - a) * 0.794) * marge1)) and b <= (a + (((x - a) * 0.778) * marge2)) 
b_c_br = cl and c >= (b - (((b - a) * 0.886) * marge2)) and c <= (b - (((b - a) * 0.382) * marge1)) 
b_d_br = dh and d >= (a + (((b - a) * 1.618) * marge2)) and d <= (a + (((b - a) * 2.618) * marge2))

//- Point B is at up to 78.6% retracement of XA.
//- Point C can be at the 38.2%-88.6% retracement of AB.
//- Point D can be found at the 161.8%-261.8% extension of AB or at the 127.2%-161.8% extension of XA. 
// The difference from a Gartley pattern is that D is not at the retracement of XA but at its extension.

b_br = b_b_br and b_c_br and b_d_br
plot_b_br = b_br and not b_br[1] ? b_br : na
plotchar(butterfly and show_anim ? plot_b_br : na, char="🦋", location=location.top, color=color.red, transp=0, size=size.small, title="Butterfly Bearish")

// Take Profit lines Butterfly

// The entry is at the point D, which is a potential reversal zone. Take Profit may be at 61.8% of CD (TP_1b), and/or
// at 127.2% of CD. You can also target points B (TP_3b) (a conservative approach) and A (TP_4b) (an aggressive approach). 
// Put a Stop Loss in line with your rules of risk management.

ENTRYb = dl and b_bl ? d : dh and b_br ? d : na
TP_1b = dl and b_bl ? valuewhen(tp_0_618a, tp_0_618a, 0) : dh and b_br ? valuewhen(tp0_618a, tp0_618a, 0) : na
TP_2b = dl and b_bl ? valuewhen(tp_1_272, tp_1_272, 0) : dh and b_br ? valuewhen(tp1_272, tp1_272, 0) : na
TP_3b = dl and b_bl ? b : dh and b_br ? b : na
TP_4b = dl and b_bl ? a : dh and b_br ? a : na


// SHARK

// Shark Bullish

s_c_bl = ch and c <= (b + (((a - b) * 1.618) * marge2)) and c >= (b + (((a - b) * 1.13) * marge1)) 
s_d_bl = dl and d <= (a - (((a - x) * 0.886) * marge2)) and d >= (a - (((a - x) * 1.13) * marge2))
s_d_bl_ = dl and d <= (c - (((c - b) * 1.618) * marge2)) and d >= (c - (((c - b) * 2.24) * marge2))

//- There’s no specific place for b (original shark b = 'a')
//- Point c (original shark c = 'b') is at the 113%-161.8% extension of ab (original shark ab = 'xa')
//- Point d (original shark d = 'c') is at the 88.6%-113% extension of xa (original shark xa = '0x') 
// and at the 161.8%-224% extension of bc (original shark bc = 'ab')

s_bl = s_c_bl and s_d_bl and s_d_bl_
plot_s_bl = s_bl and not s_bl[1] ? s_bl : na
plotchar(shark and show_anim ? plot_s_bl : na, char="🦈", location=location.bottom, color=color.lime, transp=0, size=size.small, title="Shark Bullish")

// Shark Bearish

s_c_br = cl and c >= (b - (((b - a) * 1.618) * marge2)) and c <= (b - (((b - a) * 1.13) * marge1)) 
s_d_br = dh and d >= (a + (((x - a) * 0.886) * marge2)) and d <= (a + (((x - a) * 1.13) * marge2))
s_d_br_ = dh and d >= (c + (((b - c) * 1.618) * marge2)) and d <= (c + (((b - c) * 2.24) * marge2))

//- There’s no specific place for b (original shark b = 'a')
//- Point c (original shark c = 'b') is at the 113%-161.8% extension of ab (original shark ab = 'xa')
//- Point d (original shark d = 'c') is at the 88.6%-113% extension of xa (original shark xa = '0x') 
// and at the 161.8%-224% extension of bc (original shark bc = 'ab')

s_br = s_c_br and s_d_br and s_d_br_
plot_s_br = s_br and not s_br[1] ? s_br : na
plotchar(shark and show_anim ? plot_s_br : na, char="🦈", location=location.top, color=color.red, transp=0, size=size.small, title="Shark Bearish")

// The approach to trading a Shark pattern is a bit different from that we designed for other patterns. 
// The entry is at 88.6% of xa (original shark xa = '0x'). The Take Profit can be at 50%-61.8% of cd (original shark cd = 'bc') 
// The Stop Loss should be at the point d (original shark d = 'c')

ENTRYs = dl and s_bl ? valuewhen(e_0_886, e_0_886, 0) : dh and s_br ? valuewhen(e0_886, e0_886, 0) : na
TP_1s = dl and s_bl ? valuewhen(tp_0_5, tp_0_5, 0) : dh and s_br ? valuewhen(tp0_5, tp0_5, 0) : na
TP_2s = dl and s_bl ? valuewhen(tp_0_618a, tp_0_618a, 0) : dh and s_br ? valuewhen(tp0_618a, tp0_618a, 0) : na
SLs = dl and s_bl ? d : dh and s_br ? d : na


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Labels and Lines

lev = input(75, title="Distance TP label")
invers = input(false, title="Invers label colour?"   )
lw = input(2, minval=0, maxval=10, title="TP linewidth")
lwd = input(7, minval=0, maxval=30, title="Drawings linewidth")
choice_line_br = input("red" , title="Bearish lines", options=["red", "orange", "yellow", "green", "lime", "aqua", "blue", "purple", "fuchsia", "black", "white"])
choice_line_bl = input("lime", title="Bullish lines", options=["red", "orange", "yellow", "green", "lime", "aqua", "blue", "purple", "fuchsia", "black", "white"])

label = invers ? color.new(color.white, 60) : color.new(color.black, 60)                                          
text  = invers ? color.new(color.black, 0) : color.new(color.white, 0)
textyellow = color.new(color.yellow, 0)

line_red = color.new(color.red, 0)

choice_line_tp1 = input("yellow", title="TP line 1", options=["red", "orange", "yellow", "green", "lime", "aqua", "blue", "purple", "fuchsia", "black", "white"])
choice_line_tp2 = input("white" , title="TP line 2", options=["red", "orange", "yellow", "green", "lime", "aqua", "blue", "purple", "fuchsia", "black", "white"])
choice_line_tp3 = input("lime"  , title="TP line 3", options=["red", "orange", "yellow", "green", "lime", "aqua", "blue", "purple", "fuchsia", "black", "white"])
choice_line_tp4 = input("orange", title="TP line 4", options=["red", "orange", "yellow", "green", "lime", "aqua", "blue", "purple", "fuchsia", "black", "white"])

line_yellow = 
 choice_line_tp1 == "red"     ? color.new(color.red, 0) : 
 choice_line_tp1 == "orange"  ? color.new(color.orange, 0) : 
 choice_line_tp1 == "yellow"  ? color.new(color.yellow, 0) : 
 choice_line_tp1 == "green"   ? color.new(color.green, 0) : 
 choice_line_tp1 == "lime"    ? color.new(color.lime, 0) : 
 choice_line_tp1 == "aqua"    ? color.new(color.aqua, 0) : 
 choice_line_tp1 == "blue"    ? color.new(color.blue, 0) : 
 choice_line_tp1 == "purple"  ? color.new(color.purple, 0) : 
 choice_line_tp1 == "fuchsia" ? color.new(color.fuchsia, 0) : 
 choice_line_tp1 == "black"   ? color.new(color.black, 0) : 
 choice_line_tp1 == "white"   ? color.new(color.white, 0) : na

line_white = 
 choice_line_tp2 == "red"     ? color.new(color.red, 0) : 
 choice_line_tp2 == "orange"  ? color.new(color.orange, 0) : 
 choice_line_tp2 == "yellow"  ? color.new(color.yellow, 0) : 
 choice_line_tp2 == "green"   ? color.new(color.green, 0) : 
 choice_line_tp2 == "lime"    ? color.new(color.lime, 0) : 
 choice_line_tp2 == "aqua"    ? color.new(color.aqua, 0) : 
 choice_line_tp2 == "blue"    ? color.new(color.blue, 0) : 
 choice_line_tp2 == "purple"  ? color.new(color.purple, 0) : 
 choice_line_tp2 == "fuchsia" ? color.new(color.fuchsia, 0) : 
 choice_line_tp2 == "black"   ? color.new(color.black, 0) : 
 choice_line_tp2 == "white"   ? color.new(color.white, 0) : na

line_lime = 
 choice_line_tp3 == "red"     ? color.new(color.red, 0) : 
 choice_line_tp3 == "orange"  ? color.new(color.orange, 0) : 
 choice_line_tp3 == "yellow"  ? color.new(color.yellow, 0) : 
 choice_line_tp3 == "green"   ? color.new(color.green, 0) : 
 choice_line_tp3 == "lime"    ? color.new(color.lime, 0) : 
 choice_line_tp3 == "aqua"    ? color.new(color.aqua, 0) : 
 choice_line_tp3 == "blue"    ? color.new(color.blue, 0) : 
 choice_line_tp3 == "purple"  ? color.new(color.purple, 0) : 
 choice_line_tp3 == "fuchsia" ? color.new(color.fuchsia, 0) : 
 choice_line_tp3 == "black"   ? color.new(color.black, 0) : 
 choice_line_tp3 == "white"   ? color.new(color.white, 0) : na

line_orange = 
 choice_line_tp4 == "red"     ? color.new(color.red, 0) : 
 choice_line_tp4 == "orange"  ? color.new(color.orange, 0) : 
 choice_line_tp4 == "yellow"  ? color.new(color.yellow, 0) : 
 choice_line_tp4 == "green"   ? color.new(color.green, 0) : 
 choice_line_tp4 == "lime"    ? color.new(color.lime, 0) : 
 choice_line_tp4 == "aqua"    ? color.new(color.aqua, 0) : 
 choice_line_tp4 == "blue"    ? color.new(color.blue, 0) : 
 choice_line_tp4 == "purple"  ? color.new(color.purple, 0) : 
 choice_line_tp4 == "fuchsia" ? color.new(color.fuchsia, 0) : 
 choice_line_tp4 == "black"   ? color.new(color.black, 0) : 
 choice_line_tp4 == "white"   ? color.new(color.white, 0) : na

line_red1 = 
 choice_line_br == "red"     ? color.new(color.red, 45) : 
 choice_line_br == "orange"  ? color.new(color.orange, 45) : 
 choice_line_br == "yellow"  ? color.new(color.yellow, 45) : 
 choice_line_br == "green"   ? color.new(color.green, 45) : 
 choice_line_br == "lime"    ? color.new(color.lime, 45) : 
 choice_line_br == "aqua"    ? color.new(color.aqua, 45) : 
 choice_line_br == "blue"    ? color.new(color.blue, 45) : 
 choice_line_br == "purple"  ? color.new(color.purple, 45) : 
 choice_line_br == "fuchsia" ? color.new(color.fuchsia, 45) : 
 choice_line_br == "black"   ? color.new(color.black, 45) : 
 choice_line_br == "white"   ? color.new(color.white, 45) : na

line_lime1 = 
 choice_line_bl == "red"     ? color.new(color.red, 45) : 
 choice_line_bl == "orange"  ? color.new(color.orange, 45) : 
 choice_line_bl == "yellow"  ? color.new(color.yellow, 45) : 
 choice_line_bl == "green"   ? color.new(color.green, 45) : 
 choice_line_bl == "lime"    ? color.new(color.lime, 45) : 
 choice_line_bl == "aqua"    ? color.new(color.aqua, 45) : 
 choice_line_bl == "blue"    ? color.new(color.blue, 45) : 
 choice_line_bl == "purple"  ? color.new(color.purple, 45) : 
 choice_line_bl == "fuchsia" ? color.new(color.fuchsia, 45) : 
 choice_line_bl == "black"   ? color.new(color.black, 45) : 
 choice_line_bl == "white"   ? color.new(color.white, 45) : na

//phigh = pivothigh(ABCD_br ? zigzag : na, 0, 0)
//plow = pivotlow(ABCD_bl ? zigzag : na, 0, 0)
phighcr = pivothigh(cr_br ? zigzag : na, 0, 0)
plowcr = pivotlow(cr_bl ? zigzag : na, 0, 0)
phighbt = pivothigh(bt_br ? zigzag : na, 0, 0)
plowbt = pivotlow(bt_bl ? zigzag : na, 0, 0)
phighbtA = pivothigh(bt_brA ? zigzag : na, 0, 0)
plowbtA = pivotlow(bt_blA ? zigzag : na, 0, 0)
//phighg = pivothigh(g_br ? zigzag : na, 0, 0)
//plowg = pivotlow(g_bl ? zigzag : na, 0, 0)
phighb = pivothigh(b_br ? zigzag : na, 0, 0)
plowb = pivotlow(b_bl ? zigzag : na, 0, 0)
phighs = pivothigh(s_br ? zigzag : na, 0, 0)
plows = pivotlow(s_bl ? zigzag : na, 0, 0)
//val0_382 = valuewhen(tp0_382, tp0_382, 0)                                       
//val_0_382 = valuewhen(tp_0_382, tp_0_382, 0)                                    
val0_618 = valuewhen(tp0_618, tp0_618, 0)                                       
val0_618a = valuewhen(tp0_618a, tp0_618a, 0)                                    
val_0_618 = valuewhen(tp_0_618, tp_0_618, 0)                                    
val_0_618a = valuewhen(tp_0_618a, tp_0_618a, 0)                                 
val1_272 = valuewhen(tp1_272, tp1_272, 0)                                       
val_1_272 = valuewhen(tp_1_272, tp_1_272, 0)  
val0_886 = valuewhen(tp0_886, tp0_886, 0)
val_0_886 = valuewhen(tp_0_886, tp_0_886, 0)
eval0_886 = valuewhen(e0_886, e0_886, 0)
eval_0_886 =  valuewhen(e_0_886, e_0_886, 0)
val0_5 = valuewhen(tp0_5, tp0_5, 0)
val_0_5 = valuewhen(tp_0_5, tp_0_5, 0)

_to = input(100, minval=100, title="Period Drawings")

// Functions Drawings

f_BIh(len_, x_) =>
    BIh = 0
    for i = 1 to len_
        if high[i] == x_
            break
        BIh := BIh + 1
        BIh
    BIh

f_BIl(len_, x_) =>
    BIl = 0
    for i = 1 to len_
        if low[i] == x_
            break
        BIl := BIl + 1
        BIl
    BIl

// Drawings Bullish

BIch = f_BIh(_to, c)
BIbl = f_BIl(_to, b)
BIah = f_BIh(_to, a)
BIxl = f_BIl(_to, x)

// Drawings Bearish

BIcl = f_BIl(_to, c)
BIbh = f_BIh(_to, b)
BIal = f_BIl(_to, a)
BIxh = f_BIh(_to, x)

//BIch = 0                                                                        // bar_index = 0
//for i = 0 to _to                                                                // number of bars back 0 to _to
//    if high[i] == c                                                             // if high equals c > take number of bars
//        break    
//    BIch := BIch + 1                                                            // count + 1 > this is used in bar_index to know where to plot the points

// ABCD Bearish
//if phigh
//    label1 = abcd and show_L ? label.new(bar_index[1], HH + HH/lev, text="ABCD" + "\nTP1 " + tostring(TP_1) + "\nTP2 " + tostring(TP_2) + "\nTP3 " + tostring(TP_3), textcolor=text, style=label.style_labeldown, color=label, size=SIZE) : na
//    line1 = abcd and show_TP ? line.new(bar_index[2], val0_382, bar_index, val0_382, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
//    line2 = abcd and show_TP ? line.new(bar_index[2], val0_618, bar_index, val0_618, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
//    line3 = abcd and show_TP ? line.new(bar_index[2], a, bar_index, a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
//    line4 = abcd and show_D ? line.new(bar_index[BIal], a, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line5 = abcd and show_D ? line.new(bar_index[BIal], a, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line6 = abcd and show_D ? line.new(bar_index[BIbh], b, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line7 = abcd and show_D ? line.new(bar_index[BIbh], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line8 = abcd and show_D ? line.new(bar_index[BIcl], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line.set_width(line1, lw)
//    line.set_width(line2, lw)
//    line.set_width(line3, lw)
//    line.set_width(line4, lwd)
//    line.set_width(line5, lwd)
//    line.set_width(line6, lwd)
//    line.set_width(line7, lwd)
//    line.set_width(line8, lwd)
    
// ABCD Bullish  
//if plow
//    label1 = abcd and show_L ? label.new(bar_index[1], LL - LL/lev, text="ABCD" + "\nTP1 " + tostring(TP_1) + "\nTP2 " + tostring(TP_2) + "\nTP3 " + tostring(TP_3), textcolor=text, style=label.style_labelup, color=label, size=SIZE) : na
//    line1 = abcd and show_TP ? line.new(bar_index[2], val_0_382, bar_index, val_0_382, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
//    line2 = abcd and show_TP ? line.new(bar_index[2], val_0_618, bar_index, val_0_618, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
//    line3 = abcd and show_TP ? line.new(bar_index[2], a, bar_index, a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
//    line4 = abcd and show_D ? line.new(bar_index[BIah], a, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line5 = abcd and show_D ? line.new(bar_index[BIah], a, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line6 = abcd and show_D ? line.new(bar_index[BIbl], b, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line7 = abcd and show_D ? line.new(bar_index[BIbl], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line8 = abcd and show_D ? line.new(bar_index[BIch], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line.set_width(line1, lw)
//    line.set_width(line2, lw)
//    line.set_width(line3, lw)
//    line.set_width(line4, lwd)
//    line.set_width(line5, lwd)
//    line.set_width(line6, lwd)
//    line.set_width(line7, lwd)
//    line.set_width(line8, lwd)
    
// CRAB Bearish
if phighcr
    label1 = crab and show_L ? label.new(bar_index[1], HH + HH/lev, text="CRAB" + "\nENTRY " + tostring(ENTRYcr) + "\nTP1 " + tostring(TP_1cr) + "\nTP2 " + tostring(TP_2cr), textcolor=text, style=label.style_labeldown, color=label, size=SIZE) : na
    line1 = crab and show_TP ? line.new(bar_index[2], val0_618a, bar_index, val0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = crab and show_TP ? line.new(bar_index[2], val1_272, bar_index, val1_272, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = crab and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line4 = crab and show_D ? line.new(bar_index[BIxh], x, bar_index[BIal], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line5 = crab and show_D ? line.new(bar_index[BIxh], x, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line6 = crab and show_D ? line.new(bar_index[BIal], a, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line7 = crab and show_D ? line.new(bar_index[BIbh], b, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line8 = crab and show_D ? line.new(bar_index[BIbh], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line9 = crab and show_D ? line.new(bar_index[BIcl], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line.set_style(line3, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lwd)
    line.set_width(line5, lwd)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)

// CRAB Bullish
if plowcr
    label1 = crab and show_L ? label.new(bar_index[1], LL - LL/lev, text="CRAB" + "\nENTRY " + tostring(ENTRYcr) + "\nTP1 " + tostring(TP_1cr) + "\nTP2 " + tostring(TP_2cr), textcolor=text, style=label.style_labelup, color=label, size=SIZE) : na
    line1 = crab and show_TP ? line.new(bar_index[2], val_0_618a, bar_index, val_0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = crab and show_TP ? line.new(bar_index[2], val_1_272, bar_index, val_1_272, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = crab and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line4 = crab and show_D ? line.new(bar_index[BIxl], x, bar_index[BIah], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line5 = crab and show_D ? line.new(bar_index[BIxl], x, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line6 = crab and show_D ? line.new(bar_index[BIah], a, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line7 = crab and show_D ? line.new(bar_index[BIbl], b, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line8 = crab and show_D ? line.new(bar_index[BIbl], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line9 = crab and show_D ? line.new(bar_index[BIch], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line.set_style(line3, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lwd)
    line.set_width(line5, lwd)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)

// BAT Bearish    
if phighbt
    label1 = bat and show_L ? label.new(bar_index[1], HH + HH/lev, text="BAT" + "\nENTRY " + tostring(ENTRYbt) + "\nTP1 " + tostring(TP_1bt) + "\nTP2 " + tostring(TP_2bt) + "\nTP3 " + tostring(TP_3bt), textcolor=text, style=label.style_labeldown, color=label, size=SIZE) : na
    line1 = bat and show_TP ? line.new(bar_index[2], val0_618a, bar_index, val0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = bat and show_TP ? line.new(bar_index[2], val1_272, bar_index, val1_272, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = bat and show_TP ? line.new(bar_index[2], d - (x - a), bar_index, d - (x - a), xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line4 = bat and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line5 = bat and show_D ? line.new(bar_index[BIxh], x, bar_index[BIal], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line6 = bat and show_D ? line.new(bar_index[BIxh], x, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line7 = bat and show_D ? line.new(bar_index[BIal], a, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line8 = bat and show_D ? line.new(bar_index[BIbh], b, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line9 = bat and show_D ? line.new(bar_index[BIbh], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line10 = bat and show_D ? line.new(bar_index[BIcl], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line.set_style(line4, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lw)
    line.set_width(line5, lwd)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)

// BAT Bullish
if plowbt
    label1 = bat and show_L ? label.new(bar_index[1], LL - LL/lev, text="BAT" + "\nENTRY " + tostring(ENTRYbt) + "\nTP1 " + tostring(TP_1bt) + "\nTP2 " + tostring(TP_2bt) + "\nTP3 " + tostring(TP_3bt), textcolor=text, style=label.style_labelup, color=label, size=SIZE) : na
    line1 = bat and show_TP ? line.new(bar_index[2], val_0_618a, bar_index, val_0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = bat and show_TP ? line.new(bar_index[2], val_1_272, bar_index, val_1_272, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = bat and show_TP ? line.new(bar_index[2], d + (a - x), bar_index, d + (a - x), xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line4 = bat and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line5 = bat and show_D ? line.new(bar_index[BIxl], x, bar_index[BIah], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line6 = bat and show_D ? line.new(bar_index[BIxl], x, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line7 = bat and show_D ? line.new(bar_index[BIah], a, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line8 = bat and show_D ? line.new(bar_index[BIbl], b, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line9 = bat and show_D ? line.new(bar_index[BIbl], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line10 = bat and show_D ? line.new(bar_index[BIch], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line.set_style(line4, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lw)
    line.set_width(line5, lwd)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)

// BAT ALT Bearish    
if phighbtA
    label1 = batA and show_L ? label.new(bar_index[1], HH + HH/lev, text="BAT ALT" + "\nENTRY " + tostring(ENTRYbtA) + "\nTP1 " + tostring(TP_1btA) + "\nTP2 " + tostring(TP_2btA) + "\nTP3 " + tostring(TP_3btA) + "\nTP4 " + tostring(TP_4btA), textcolor=text, style=label.style_labeldown, color=label, size=SIZE) : na
    line1 = batA and show_TP ? line.new(bar_index[2], val0_618a, bar_index, val0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = batA and show_TP ? line.new(bar_index[2], val0_886, bar_index, val0_886, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = batA and show_TP ? line.new(bar_index[2], b, bar_index, b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line4 = batA and show_TP ? line.new(bar_index[2], c, bar_index, c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_orange) : na
    line5 = batA and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line6 = batA and show_D ? line.new(bar_index[BIxh], x, bar_index[BIal], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line7 = batA and show_D ? line.new(bar_index[BIxh], x, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line8 = batA and show_D ? line.new(bar_index[BIal], a, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line9 = batA and show_D ? line.new(bar_index[BIbh], b, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line10 = batA and show_D ? line.new(bar_index[BIbh], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line11 = batA and show_D ? line.new(bar_index[BIcl], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line.set_style(line5, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lw)
    line.set_width(line5, lw)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)
    line.set_width(line11, lwd)

// BAT ALT Bullish
if plowbtA
    label1 = batA and show_L ? label.new(bar_index[1], LL - LL/lev, text="BAT ALT" + "\nENTRY " + tostring(ENTRYbtA) + "\nTP1 " + tostring(TP_1btA) + "\nTP2 " + tostring(TP_2btA) + "\nTP3 " + tostring(TP_3btA) + "\nTP4 " + tostring(TP_4btA), textcolor=text, style=label.style_labelup, color=label, size=SIZE) : na
    line1 = batA and show_TP ? line.new(bar_index[2], val_0_618a, bar_index, val_0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = batA and show_TP ? line.new(bar_index[2], val_0_886 , bar_index, val_0_886 , xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = batA and show_TP ? line.new(bar_index[2], b, bar_index, b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line4 = batA and show_TP ? line.new(bar_index[2], c, bar_index, c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_orange) : na
    line5 = batA and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line6 = batA and show_D ? line.new(bar_index[BIxl], x, bar_index[BIah], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line7 = batA and show_D ? line.new(bar_index[BIxl], x, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line8 = batA and show_D ? line.new(bar_index[BIah], a, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line9 = batA and show_D ? line.new(bar_index[BIbl], b, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line10 = batA and show_D ? line.new(bar_index[BIbl], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line11 = batA and show_D ? line.new(bar_index[BIch], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line.set_style(line5, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lw)
    line.set_width(line5, lw)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)
    line.set_width(line11, lwd)

// Gartley Bearish    
//if phighg
//    label1 = gartley and show_L ? label.new(bar_index[1], HH + HH/lev, text="Gartley" + "\nENTRY " + tostring(ENTRYg) + "\nTP1 " + tostring(TP_1g) + "\nTP2 " + tostring(TP_2g) + "\nSL " + tostring(SL_1g), textcolor=text, style=label.style_labeldown, color=label, size=SIZE) : na
//    line1 = gartley and show_TP ? line.new(bar_index[2], val0_618a, bar_index, val0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na  // TP1
//    line2 = gartley and show_TP ? line.new(bar_index[2], d - (x - a), bar_index, d - (x - a), xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na // TP2
//    line3 = gartley and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na  // = ENTRY
//    line4 = gartley and show_SL ? line.new(bar_index[2], x + (x / 100), bar_index, x + (x / 100), xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red) : na  // SL
//    line5 = gartley and show_D ? line.new(bar_index[BIxh], x, bar_index[BIal], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line6 = gartley and show_D ? line.new(bar_index[BIxh], x, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line7 = gartley and show_D ? line.new(bar_index[BIal], a, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line8 = gartley and show_D ? line.new(bar_index[BIbh], b, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line9 = gartley and show_D ? line.new(bar_index[BIbh], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line10 = gartley and show_D ? line.new(bar_index[BIcl], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
//    line.set_style(line3, line.style_arrow_left)  // ENTRY
//    line.set_style(line4, line.style_dashed)
//    line.set_width(line1, lw)
//    line.set_width(line2, lw)
//    line.set_width(line3, lw)
//    line.set_width(line4, lw)
//    line.set_width(line5, lwd)
//    line.set_width(line6, lwd)
//    line.set_width(line7, lwd)
//    line.set_width(line8, lwd)
//    line.set_width(line9, lwd)
//    line.set_width(line10, lwd)
    
// Gartley Bullish
//if plowg
//    label1 = gartley and show_L ? label.new(bar_index[1], LL - LL/lev, text="Gartley" + "\nENTRY " + tostring(ENTRYg) + "\nTP1 " + tostring(TP_1g) + "\nTP2 " + tostring(TP_2g) + "\nSL " + tostring(SL_1g), textcolor=text, style=label.style_labelup, color=label, size=SIZE) : na
//    line1 = gartley and show_TP ? line.new(bar_index[2], val_0_618a, bar_index, val_0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
//    line2 = gartley and show_TP ? line.new(bar_index[2], d + (a - x), bar_index, d + (a - x), xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
//    line3 = gartley and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
//    line4 = gartley and show_SL ? line.new(bar_index[2], x - (x / 100), bar_index, x - (x / 100), xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red) : na
//    line5 = gartley and show_D ? line.new(bar_index[BIxl], x, bar_index[BIah], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line6 = gartley and show_D ? line.new(bar_index[BIxl], x, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line7 = gartley and show_D ? line.new(bar_index[BIah], a, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line8 = gartley and show_D ? line.new(bar_index[BIbl], b, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line9 = gartley and show_D ? line.new(bar_index[BIbl], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line10 = gartley and show_D ? line.new(bar_index[BIch], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
//    line.set_style(line3, line.style_arrow_left)
//    line.set_style(line4, line.style_dashed)
//    line.set_width(line1, lw)
//    line.set_width(line2, lw)
//    line.set_width(line3, lw)
//    line.set_width(line4, lw)
//    line.set_width(line5, lwd)
//    line.set_width(line6, lwd)
//    line.set_width(line7, lwd)
//    line.set_width(line8, lwd)
//    line.set_width(line9, lwd)
//    line.set_width(line10, lwd)

// Butterfly Bearish
if phighb
    label1 = butterfly and show_L ? label.new(bar_index[1], HH + HH/lev, text="Butterfly" + "\nENTRY " + tostring(ENTRYb) + "\nTP1 " + tostring(TP_1b) + "\nTP2 " + tostring(TP_2b) + "\nTP3 " + tostring(TP_3b) + "\nTP4 " + tostring(TP_4b), textcolor=text, style=label.style_labeldown, color=label, size=SIZE) : na
    line1 = butterfly and show_TP ? line.new(bar_index[2], val0_618a, bar_index, val0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = butterfly and show_TP ? line.new(bar_index[2], val1_272, bar_index, val1_272, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = butterfly and show_TP ? line.new(bar_index[2], b, bar_index, b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line4 = butterfly and show_TP ? line.new(bar_index[2], a, bar_index, a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_orange) : na
    line5 = butterfly and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line6 = butterfly and show_D ? line.new(bar_index[BIxh], x, bar_index[BIal], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line7 = butterfly and show_D ? line.new(bar_index[BIxh], x, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line8 = butterfly and show_D ? line.new(bar_index[BIal], a, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line9 = butterfly and show_D ? line.new(bar_index[BIbh], b, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line10 = butterfly and show_D ? line.new(bar_index[BIbh], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line11 = butterfly and show_D ? line.new(bar_index[BIcl], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line.set_style(line5, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lw)
    line.set_width(line5, lw)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)
    line.set_width(line11, lwd)

// Butterfly Bullish
if plowb
    label1 = butterfly and show_L ? label.new(bar_index[1], LL - LL/lev, text="Butterfly" + "\nENTRY " + tostring(ENTRYb) + "\nTP1 " + tostring(TP_1b) + "\nTP2 " + tostring(TP_2b)+ "\nTP3 " + tostring(TP_3b) + "\nTP4 " + tostring(TP_4b), textcolor=text, style=label.style_labelup, color=label, size=SIZE) : na
    line1 = butterfly and show_TP ? line.new(bar_index[2], val_0_618a, bar_index, val_0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line2 = butterfly and show_TP ? line.new(bar_index[2], val_1_272, bar_index, val_1_272, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_white) : na
    line3 = butterfly and show_TP ? line.new(bar_index[2], b, bar_index, b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line4 = butterfly and show_TP ? line.new(bar_index[2], a, bar_index, a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_orange) : na
    line5 = butterfly and show_E ? line.new(bar_index[1], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line6 = butterfly and show_D ? line.new(bar_index[BIxl], x, bar_index[BIah], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line7 = butterfly and show_D ? line.new(bar_index[BIxl], x, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line8 = butterfly and show_D ? line.new(bar_index[BIah], a, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line9 = butterfly and show_D ? line.new(bar_index[BIbl], b, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line10 = butterfly and show_D ? line.new(bar_index[BIbl], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line11 = butterfly and show_D ? line.new(bar_index[BIch], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line.set_style(line5, line.style_arrow_left)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)   
    line.set_width(line4, lw)
    line.set_width(line5, lw)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)
    line.set_width(line11, lwd)

// SHARK Bearish
if phighs
    label1 = shark and show_L ? label.new(bar_index[1], HH + HH/lev, text="SHARK" + "\nENTRY " + tostring(ENTRYs) + "\nTP1 " + tostring(TP_1s) + "\nTP2 " + tostring(TP_2s) + "\nSL " + tostring(SLs), textcolor=text, style=label.style_labeldown, color=label, size=SIZE) : na
    line1 = shark and show_TP ? line.new(bar_index[2], val0_618a, bar_index, val0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line2 = shark and show_TP ? line.new(bar_index[2], val0_5, bar_index, val0_5, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line3 = shark and show_E ? line.new(bar_index[1], eval0_886, bar_index, eval0_886, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line4 = shark and show_SL ? line.new(bar_index[2], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red) : na
    line5 = shark and show_D ? line.new(bar_index[BIxh], x, bar_index[BIal], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line6 = shark and show_D ? line.new(bar_index[BIxh], x, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line7 = shark and show_D ? line.new(bar_index[BIal], a, bar_index[BIbh], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line8 = shark and show_D ? line.new(bar_index[BIbh], b, bar_index[BIcl], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line9 = shark and show_D ? line.new(bar_index[BIbh], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line10 = shark and show_D ? line.new(bar_index[BIcl], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red1) : na
    line.set_style(line3, line.style_arrow_left)
    line.set_style(line4, line.style_dashed)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lw)
    line.set_width(line5, lwd)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)

// SHARK Bullish
if plows
    label1 = shark and show_L ? label.new(bar_index[1], LL - LL/lev, text="SHARK" + "\nENTRY " + tostring(ENTRYs) + "\nTP1 " + tostring(TP_1s) + "\nTP2 " + tostring(TP_2s) + "\nSL " + tostring(SLs), textcolor=text, style=label.style_labelup, color=label, size=SIZE) : na
    line1 = shark and show_TP ? line.new(bar_index[2], val_0_618a, bar_index, val_0_618a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_yellow) : na
    line2 = shark and show_TP ? line.new(bar_index[2], val_0_5, bar_index, val_0_5, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime) : na
    line3 = shark and show_E ? line.new(bar_index[1], eval_0_886, bar_index, eval_0_886, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=color.white) : na
    line4 = shark and show_SL ? line.new(bar_index[2], d, bar_index, d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_red) : na
    line5 = shark and show_D ? line.new(bar_index[BIxl], x, bar_index[BIah], a, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line6 = shark and show_D ? line.new(bar_index[BIxl], x, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line7 = shark and show_D ? line.new(bar_index[BIah], a, bar_index[BIbl], b, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line8 = shark and show_D ? line.new(bar_index[BIbl], b, bar_index[BIch], c, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line9 = shark and show_D ? line.new(bar_index[BIbl], b, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line10 = shark and show_D ? line.new(bar_index[BIch], c, bar_index[1], d, xloc = xloc.bar_index, style=line.style_solid, extend=extend.none, color=line_lime1) : na
    line.set_style(line3, line.style_arrow_left)
    line.set_style(line4, line.style_dashed)
    line.set_width(line1, lw)
    line.set_width(line2, lw)
    line.set_width(line3, lw)
    line.set_width(line4, lw)
    line.set_width(line5, lwd)
    line.set_width(line6, lwd)
    line.set_width(line7, lwd)
    line.set_width(line8, lwd)
    line.set_width(line9, lwd)
    line.set_width(line10, lwd)

// Alerts

//ABCD_bl_alert = ABCD_bl and not ABCD_bl[1] ? true : na
//alertcondition(ABCD_bl_alert, title='ABCD bullish Alert', message='ABCD bullish Alert')

//ABCD_br_alert = ABCD_br and not ABCD_br[1] ? true : na
//alertcondition(ABCD_br_alert, title='ABCD bearish Alert', message='ABCD bearish Alert')

cr_bl_alert = cr_bl and not cr_bl[1] ? true : na
alertcondition(cr_bl_alert, title='Crab bullish Alert', message='Crab bullish Alert')

cr_br_alert = cr_br and not cr_br[1] ? true : na
alertcondition(cr_br_alert, title='Crab bearish Alert', message='Crab bearish Alert')

cr_bl_strong_alert = cr_bl_strong and not cr_bl_strong[1] ? true : na
alertcondition(cr_bl_strong_alert, title='Crab strong bullish Alert', message='Crab strong bullish Alert')

cr_br_strong_alert = cr_br_strong and not cr_br_strong[1] ? true : na
alertcondition(cr_br_strong_alert, title='Crab strong bearish Alert', message='Crab strong bearish Alert')

bt_bl_alert = bt_bl and not bt_bl[1] ? true : na
alertcondition(bt_bl_alert, title='Bat bullish Alert', message='Bat bullish Alert')

bt_br_alert = bt_br and not bt_br[1] ? true : na
alertcondition(bt_br_alert, title='Bat bearish Alert', message='Bat bearish Alert')

//g_bl_alert = g_bl and not g_bl[1] ? true : na
//alertcondition(g_bl_alert, title='Gartley bullish Alert', message='Gartley bullish Alert')

//g_br_alert = g_br and not g_br[1] ? true : na
//alertcondition(g_br_alert, title='Gartley bearish Alert', message='Gartley bearish Alert')

b_bl_alert = b_bl and not b_bl[1] ? true : na
alertcondition(b_bl_alert, title='Butterfly bullish Alert', message='Butterfly bullish Alert')

b_br_alert = b_br and not b_br[1] ? true : na
alertcondition(b_br_alert, title='Butterfly bearish Alert', message='Butterfly bearish Alert')

s_bl_alert = s_bl and not s_bl[1] ? true : na
alertcondition(s_bl_alert, title='Shark bullish Alert', message='Shark bullish Alert')

s_br_alert = s_br and not s_br[1] ? true : na
alertcondition(s_br_alert, title='Shark bearish Alert', message='Shark bearish Alert')

something = (s_bl and not s_bl[1]) or (s_br and not s_br[1]) or (b_bl and not b_bl[1]) or (b_br and not b_br[1]) or (bt_bl and not bt_bl[1]) or (bt_br and not bt_br[1]) or (cr_bl and not cr_bl[1]) or (cr_br and not cr_br[1]) or (cr_bl_strong and not cr_bl_strong[1]) or (cr_br_strong and not cr_br_strong[1]) ? true : na
alertcondition(something, title='"Something Alert"', message='"Something Alert" > Check chart!')


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////