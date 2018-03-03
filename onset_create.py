# -*-coding:utf-8-*-

def file_write(OUTPUT_FILENAME, Frames):
    f = open(OUTPUT_FILENAME, "w")

    for row in Frames:
        if type(row) == float:
            data = row
        else:
            data = float(row)

        f.write(str(data))
        f.write("\n")

    f.close()

def data_create(start_num, end_num, jag):
    data = []
    for i in range(int((end_num - start_num) // jag)):
        data.append(i * jag + start_num)
    return data

if __name__ == "__main__":
    output_filename = "../data/preexperiment/test/analysis/onset_time/onset_"

    start_num = 6.70
     #6.25
    end_num = 606.70
    jag = 0.25

    frames = data_create(start_num, end_num, jag)
    num = 3

    #for i in range(num):
    i = 1
    file_write(output_filename + str(i+1) + ".txt", frames)
