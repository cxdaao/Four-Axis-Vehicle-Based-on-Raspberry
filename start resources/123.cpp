//6��IMUԭʼ����
struct Mems{
    int ax;
    int ay;
    int az;
    int gx;
    int gy;
    int gz;
}
//ԭʼ���ݼ���Ƕ�
struct Angle{
    double X_Angle;
    double Y_Angle;
    double Z_Angle;
}
//ң���ź�
struct remote{
    int duty;
    float frenquence;
};
//�������
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


