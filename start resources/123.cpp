//6轴IMU原始数据
struct Mems{
    int ax;
    int ay;
    int az;
    int gx;
    int gy;
    int gz;
}
//原始数据计算角度
struct Angle{
    double X_Angle;
    double Y_Angle;
    double Z_Angle;
}
//遥控信号
struct remote{
    int duty;
    float frenquence;
};
//超声测距
struct ultrasound{
    float time;
    float speed;
};

struct gps{
    float UTCtime;
    float weidu;
    bool weidubanqiu;
    float jingdu;
    bool jingdubanqiu;
    bool quality;
    int sellitenum;
    float jingquedu;
    float haiba;
    char haibaunit;
    float tuoqiumian;
    char tuoqiumianunit;
    int rtcm;
    short sign;
    bool sum;
};

struct camera{
    int[][][3] bitmap;
};

struct wifi{
float speed;
float jingdu;
float weidu;
float haiba;
int [][][3] bitmap;
};


