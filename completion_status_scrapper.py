def completion_status(iterable_length, index):
    if ((index/iterable_length) * 100)%10 == 0:
        print('*******completed*****', str(int((index/iterable_length)*100)) + '%')