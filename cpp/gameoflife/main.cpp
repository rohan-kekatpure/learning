#include <QApplication>
#include <QPushButton>

int main(int argc, char **argv)
{
 QApplication app (argc, argv);

 QWidget window;
 window.setFixedSize(800, 500);

 QPushButton *button = new QPushButton("Hello World", &window);
 button->setGeometry(10, 10, 80, 30);

 window.show();
 return app.exec();
}