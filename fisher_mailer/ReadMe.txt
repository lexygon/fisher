bu klasör aslen django-mailer projesinin bir parçası.
ancak django-mailer maalesef tek bir smtp bilgisini kullanarak mail atabiliyor.
bunu değiştirmek için güncelledim kütüphaneyi. ancak henüz eksik olduğu için,
projeyi forktan değil de bu şekilde import ettim geçici olarak.

django-mailer standart django mail sistemini bir queue yapısı ile birleştirip cron aracılığı ile projenin kendisinden asenkron olarak
toplu mail atıp bunları manage edebilen bir kütüphanedir.