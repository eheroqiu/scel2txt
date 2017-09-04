
# coding: utf-8

# In[16]:

import struct
import sys
import binascii 
import pdb
#拼音表偏移，
startPy = 0x1540;
#汉语词组表偏移
startChinese = 0x2628;
#全局拼音表

GPy_Table ={}

#解析结果
#元组(词频,拼音,中文词组)的列表
GTable = []
def byte2str(data):
    i = 0
    length = len(data)
    ret = u''
    while i < length:
        x = data[i] + data[i+1]
        t = unichr(struct.unpack('H',x)[0])
        if t == u'r':
            ret += u'n'
        elif t != u' ':
            ret += t
        i += 2
    return ret

#读取中文表    
def getChinese(data):
    #import pdb
    #pdb.set_trace()
    
    pos = 0
    length = len(data)
    while pos < length:
        #同音词数量
        same = struct.unpack('H',data[pos]+data[pos+1])[0]
        #print '[same]:',same,
        
        #拼音索引表长度
        pos += 2
        py_table_len = struct.unpack('H',data[pos]+data[pos+1])[0]
        #拼音索引表
        pos += 2
        #py = getWordPy(data[pos: pos+py_table_len])

        #中文词组
        pos += py_table_len
        for i in xrange(same):
            #中文词组长度
            c_len = struct.unpack('H',data[pos]+data[pos+1])[0]
            #中文词组
            pos += 2  
            word = byte2str(data[pos: pos + c_len])
            #扩展数据长度
            pos += c_len        
            ext_len = struct.unpack('H',data[pos]+data[pos+1])[0]
            #词频
            pos += 2
            #count  = struct.unpack('H',data[pos]+data[pos+1])[0]

            #保存
            GTable.append((word))
        
            #到下个词的偏移位置
            pos +=  ext_len

def deal():
    print '-'*60
    f = open('C:\Users\youar\Desktop\web_words.scel','rb')
    data = f.read()
    f.close()
    #pdb.set_trace()
    
    print "词库名：" ,byte2str(data[0x130:0x338])#.encode('GB18030')
    print "词库类型：" ,byte2str(data[0x338:0x540])#.encode('GB18030')
    print "描述信息：" ,byte2str(data[0x540:0xd40])#.encode('GB18030')
    print "词库示例：",byte2str(data[0xd40:startPy])#.encode('GB18030')
    getChinese(data[startChinese:])
            
if __name__ == '__main__':
    deal()
    #保存结果  
    f = open('webwords_dict','w')
    for word in GTable:
        print word
        #GTable保存着结果，是一个列表，每个元素是一个元组(词频,拼音,中文词组)，有需要的话可以保存成自己需要个格式
        #我没排序，所以结果是按照上面输入文件的顺序
        #f.write( unicode('{%(count)s}' %{'count':count}+py+' '+ word).encode('GB18030') )
        f.write( unicode(word).encode('utf8') )
        f.write(' 22 n\n')
    f.close()     


# In[ ]:



