# The Indistinguishable-From-Magic 8 Ball
The Indistinguishable-From-Magic 8 Ball is an open source project. Provided here are the code and some build directions. Or, more precisely...the code's here, and some directions and photographs are to come. 

### Now in 2 flavours!
I exhibited a few of these devices at the [2025 ELO Conference](https://elo25.org) (big thanks to Joel Ong!). I found they were heavy on power demands and I've rewritten the code in C and C++. See [this GitHub repo](https://github.com/mysteryproducer/eightball-c) for the code. I've left these revised 8-balls switched on for about a week; I haven't run down one of the batteries yet.

### Current hardware:
*  ESP32-S3 supermini
*  Round TFT screen: 1.28" gc9a01  
*  MPU6050 accelerometer (on GY-521 module)
*  3.7V 18650 LIPO battery
*  18650 charger board with overload protection
*  USB-C female port
*  2x USB-C male connectors (optional, but these help to make the assembly modular)
*  some wire (I use 4 colours)
*  1 magic 8-ball, deseeded

### Notes:
* At the moment, soldering is required for this project. However, it's been through several iterations and it's being refined all the time. Solderless solutions are on my list of things to consider.
* It's probably not socially resonsible, but I get my parts from AliExpress. I figure AliExpress can't be much more evil than Amazon. 
* The real Mattel magic 8-ball is very well-built, and I don't recommend working with them. The cheap rip-off magic 8-balls are much easier to cut open.
