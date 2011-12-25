
object=sort.o managemem.o

bigsort:$(object)
	cc -o bigsort $(object)

sort.o:src/sort.c include/sort.h
	cc -c src/sort.c -I include
managemem.o:src/managemem.c include/managemem.h
	cc -c src/managemem.c -I include
clean:
	rm *.o
	rm bigsort
