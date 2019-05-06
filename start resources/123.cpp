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
    int duty; //占空比
    float frequence;  //频率
};
//超声测距
struct ultrasound{
    float time;
    int num; //测量次数
};

struct gps{
    float UTCtime; //UTC时间
    float latitude; //纬度，格式：ddmm.mmmm，前导位不足补0
    bool lat_hemisphere; //纬度半球，N或S
    float longitude; //经度，格式dddmm.mmmm，前导位不足补0
    bool lon_hemisphere; //经度半球，E或S 
    bool quality; //定位质量指示，0无效1有效
    int sellitenum; //使用卫星数量，0到12前导位不足补0
    float precision; //水平精确度
    float altitude; //海拔
    char alt_unit;
    float tuoqiumian; //大地椭球面相对海平面的高度
    char tuoqiumianunit; //高度单位
    int rtcm; //差分GPS数据极限
    short sign; //基站号
    bool sum; //校验位
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
