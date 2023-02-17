# written by Francesco Mambretti
# 24/01/2023

folders=(0_NH2_750K 12_NH2_750K  16_NH2_750K  4_NH2_750K  8_NH2_750K)

for f in ${folders[*]}; do
    cp *raw*sh $f
	cd $f
    n=`ls box.raw | wc -l`
	sh raw_to_set.sh $n
	cd ..
done
