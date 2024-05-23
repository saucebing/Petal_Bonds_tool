import os, re, time
from service import get_flag, set_flag
fnames = os.listdir('../Cards/')
frame_ind = '000005'
for occupation_ind in range(1, 10):
    for card_ind in range(0, 10):
        for shape_ind in range(0, 2):
            prefix = '%02d%08d_%s_%d_' % (occupation_ind, card_ind, frame_ind, shape_ind)
            fname = [fname for fname in fnames if prefix in fname][0]
            fpath = fname
            print(fname)
            os.system('cp ../Cards/%s input.png' % (fname))
            set_flag('fname', fpath)
            set_flag('flag', 'start')
            set_flag('shape_ind', str(shape_ind))
            while get_flag('flag') != 'Done':
                time.sleep(1)
            #fname_pattern = r'%02d%08d_%s_%d_(.*).png' % (occupation_ind, card_ind, frame_ind, shape_ind)
            #pat = re.compile(fname_pattern)
            #postfix = pat.findall(fname)[0]
