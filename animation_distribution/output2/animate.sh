#convert -delay 14 -loop 0 *.png animation.gif


for D in `find . -type d`
do
    (cd $D && convert -delay 14 -loop 0 *.png animation.gif)
done

