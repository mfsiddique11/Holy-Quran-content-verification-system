from django.shortcuts import render,redirect
from .models import Quran
import speech_recognition as sr
import base64
from django.http import HttpResponse
from PIL import Image
import pytesseract
from django.template import Context, Template
import time

def ajax_audio(blob):
    blob = blob.partition(",")[2]
    blob = base64.b64decode(blob)
    with open('audio.wav','wb') as recordings:
        recordings.write(blob)
        recordings.close()
    fileA = "audio.wav"
    r = sr.Recognizer()
    with sr.AudioFile(fileA) as source:
        audio=r.record(source)
        try:
            result=r.recognize_google(audio,language='ar-SA')
            return result
        except sr.UnknownValueError:
            result="Could not understand, Please try again"
            return result

def audio_F(fileA):
    r = sr.Recognizer()
    with sr.AudioFile(fileA) as source:
        audio=r.record(source)
        try:
            result=r.recognize_google(audio,language='ar-SA')
            return result
        except sr.UnknownValueError:
            result="Could not understand, Please try again"
            return result

def image_F(fileI):
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'
    image=Image.open(fileI)
    file = pytesseract.image_to_string(image, lang='ara')
    return file

def my_split(file):
    arr=[]
    str_arr=[]
    c=0
    for i in file:
        if i==' ':
            if c!=1:
                if c!=0:
                    str_arr.append(''.join(arr))
                    arr=[]
            c=0
        else:
            c=c+1
            arr.append(i)
    if c!=0:
        str_arr.append(''.join(arr))
    return str_arr

def quran_corrector(ayah):
    avt=[]
    ayah_words=[]
    temp=['َ', 'ِ', 'ُ']
    check=0
    ayah=' '.join(my_split(ayah))
    if any(x in ayah for x in temp):
        diacritics=1
        for quran in Quran.objects.all():
            if ayah in quran.ChapterArabic:
                check=1
    else:
        diacritics=0
        for quran in Quran.objects.all():
            if ayah in quran.ChapterNArabic:
                check=1
    if check==0:
        arr_verse_text=[]
        arr_p=[0]
        stringf=ayah.split()
        for quran in Quran.objects.all():
            if diacritics==1:
                stringdb1=quran.ChapterArabic
                stringdb=quran.ChapterArabic.split()
            else:
                stringdb1=quran.ChapterNArabic
                stringdb=quran.ChapterNArabic.split()
            stringf.append('a')
            stringdb.append('a')
            count_match=0
            a=0
            b=0
            while stringf[a]!='a':
                while stringdb[b]!='a':
                    if stringf[a] == stringdb[b]:
                       count_match=count_match+0.1
                    elif stringf[a] in stringdb[b]:
                        count_match=count_match+0.1
                    b=b+1
                b=0
                a=a+1
            stringdb.pop()
            a=0
            while stringf[a]!='a':
                if stringf[a+1]!='a':
                    if ' '.join(stringf[a:a+2]) in stringdb1:
                        count_match=count_match+2
                else:
                    break
                a=a+1
            a=0
            while stringf[a]!='a':
                if stringf[a+1]!='a':
                    if stringf[a+2]!='a':
                        if ' '.join(stringf[a:a+3]) in stringdb1:
                            count_match=count_match+3
                    else:
                        break
                else:
                    break
                a=a+1
            a=0
            if count_match>0:
                 if count_match not in arr_p:
                     if count_match>arr_p[0]:
                         arr_p.insert(0,count_match)
                         arr_verse_text.insert(0,stringdb1)
                     else:
                         for ind,i in enumerate(arr_p):
                             if count_match>i:
                                 arr_p.insert(ind,count_match)
                                 arr_verse_text.insert(ind,stringdb1)
                                 break
                 else:
                     for ind,i in enumerate(arr_p):
                         if count_match>i:
                             a=1
                             arr_p.insert(ind,count_match)
                             arr_verse_text.insert(ind,stringdb1)
                             break
                     if a==0:
                         arr_p.append(count_match)
                         arr_verse_text.append(stringdb1)
            stringf.pop()
        avt=list(arr_verse_text)    
        if arr_verse_text==[]:
            ayah_new_words=[]
            if diacritics==1:
                with open('awords.txt','r',encoding='utf-8') as f:
                    right=f.read().splitlines()
            else:
                with open('nawords.txt','r',encoding='utf-8') as f:
                    right=f.read().splitlines()
            ayah_words=ayah.split()
            for ayah in ayah_words:
                arr_verse_text=[]
                arr_p=[100]
                for rword in right:
                    count_match=0
                    a=0
                    b=1
                    stringf=[]
                    tmp=[]
                    for i in range(len(ayah)):
                        stringf.append(ayah[a:b])
                        tmp.append(ayah[a:b])
                        a=a+1
                        b=b+1
                    stringdb=[]
                    a=0
                    b=1
                    for i in range(len(rword)):
                        stringdb.append(rword[a:b])
                        a=a+1
                        b=b+1
                    for ind,i in enumerate(stringdb):
                        if i in stringf:
                            q=stringf.index(i)
                            del stringf[q]
                            stringf.insert(q,'a')
                            stringdb[ind]='a'
                    stringdb=list(filter(('a').__ne__, stringdb))
                    stringf=list(filter(('a').__ne__, stringf))
                    l=len(stringdb)+len(stringf)
                    if len(stringdb)==len(stringf) and l >=2:
                        count_match=count_match+l
                    a=0
                    b=2
                    stringf=[]
                    for i in range(len(ayah)-1):
                        stringf.append(ayah[a:b])
                        a=a+1
                        b=b+1
                    stringdb=[]
                    a=0
                    b=2
                    for i in range(len(rword)-1):
                        stringdb.append(rword[a:b])
                        a=a+1
                        b=b+1
                    for ind,i in enumerate(stringdb):
                        if i in stringf:
                            q=stringf.index(i)
                            del stringf[q]
                            stringf.insert(q,'a')
                            stringdb[ind]='a'
                    stringdb=list(filter(('a').__ne__, stringdb))
                    stringf=list(filter(('a').__ne__, stringf))
                    l=len(stringdb)+len(stringf)
                    stringdb1=rword
                    if len(stringdb)==len(stringf) and l >=2:
                        count_match=count_match+l
                    if count_match>0:
                        if count_match<arr_p[0]:
                            arr_p=[]
                            arr_p.insert(0,count_match)
                            arr_verse_text=[]
                            arr_verse_text.insert(0,stringdb1)
                        elif count_match==arr_p[0]:
                            arr_p.append(count_match)
                            arr_verse_text.append(stringdb1)
                ayah_new_words.append(arr_verse_text[0])
            ayah=' '.join(ayah_new_words)
        else:
            ayah_new_words=[]
            w=[]
            ccc=0
            for aya in avt:
                ccc=ccc+1
                if ccc==10:
                    break
                right=aya.split()
                stringf1=ayah.split()
                stringftmp=ayah.split()
                for ind,aua in enumerate(stringf1):
                    if aua not in right:
                        w.append(aua)
                        arr_verse_text=[]
                        arr_p=[100]
                        for rword in right:
                            a=0
                            b=1
                            stringf=[]
                            for i in range(len(aua)):
                                stringf.append(aua[a:b])
                                a=a+1
                                b=b+1
                            stringdb=[]
                            a=0
                            b=1
                            for i in range(len(rword)):
                                stringdb.append(rword[a:b])
                                a=a+1
                                b=b+1
                            count_match=0
                            for ind,i in enumerate(stringdb):
                                if i in stringf:
                                    q=stringf.index(i)
                                    del stringf[q]
                                    stringf.insert(q,'a')
                                    stringdb[ind]='a'
                            stringdb=list(filter(('a').__ne__, stringdb))
                            stringf=list(filter(('a').__ne__, stringf))
                            l=len(stringdb)+len(stringf)
                            count_match=count_match+l
                            a=0
                            b=2
                            stringf=[]
                            for i in range(len(aua)-1):
                                stringf.append(aua[a:b])
                                a=a+1
                                b=b+1
                            stringdb=[]
                            a=0
                            b=2
                            for i in range(len(rword)-1):
                                stringdb.append(rword[a:b])
                                a=a+1
                                b=b+1
                            for ind,i in enumerate(stringdb):
                                if i in stringf:
                                    q=stringf.index(i)
                                    del stringf[q]
                                    stringf.insert(q,'a')
                                    stringdb[ind]='a'
                            stringdb=list(filter(('a').__ne__, stringdb))
                            stringf=list(filter(('a').__ne__, stringf))
                            l=len(stringdb)+len(stringf)
                            count_match=count_match+l
                            a=0
                            b=3
                            stringf=[]
                            for i in range(len(aua)-2):
                                stringf.append(aua[a:b])
                                a=a+1
                                b=b+1
                            stringdb=[]
                            a=0
                            b=3
                            for i in range(len(rword)-2):
                                stringdb.append(rword[a:b])
                                a=a+1
                                b=b+1
                            for ind,i in enumerate(stringdb):
                                if i in stringf:
                                    q=stringf.index(i)
                                    del stringf[q]
                                    stringf.insert(q,'a')
                                    stringdb[ind]='a'
                            stringdb=list(filter(('a').__ne__, stringdb))
                            stringf=list(filter(('a').__ne__, stringf))
                            l=len(stringdb)+len(stringf)
                            count_match=count_match+l
                            stringdb1=rword
                            if count_match>0:
                                if count_match<arr_p[0]:
                                    arr_p=[]
                                    arr_p.insert(0,count_match)
                                    arr_verse_text=[]
                                    arr_verse_text.insert(0,stringdb1)
                                elif count_match==arr_p[0]:
                                    arr_p.append(count_match)
                                    arr_verse_text.append(stringdb1)
                        if arr_verse_text != []:
                            q=0       
                            q=stringftmp.index(aua)
                            del stringftmp[q]
                            stringftmp.insert(q,arr_verse_text[0])
                        
                if ' '.join(stringftmp) in aya:
                    ayah=' '.join(stringftmp)
                    break  
                        
    arr_chapter=[]
    arr_verse=[]
    arr_verse_text=[]
    arr_p=[0]
    stringf=ayah.split()
    for quran in Quran.objects.all():
        if diacritics==1:
            stringdb=quran.ChapterArabic.split()
            stringdb1=quran.ChapterArabic
        else:
            stringdb=quran.ChapterNArabic.split()
            stringdb1=quran.ChapterNArabic
        tmp=quran.ChapterArabic.split()
        stringf.append('a')
        stringdb.append('a')
        count_match=0
        a=0
        b=0
        while stringf[a]!='a':
            while stringdb[b]!='a':
                if stringf[a] == stringdb[b]:
                   t = Template('<span style="color:red">{{message}}</span>')
                   cn = Context({'message': tmp[b]})
                   html = t.render(cn)
                   tmp[b]=html
                   count_match=count_match+0.1
                elif stringf[a] in stringdb[b]:
                    t = Template('<span style="color:red">{{message}}</span>')
                    cn = Context({'message': tmp[b]})
                    html = t.render(cn)
                    tmp[b]=html
                    count_match=count_match+0.1
                b=b+1
            b=0
            a=a+1
        stringdb.pop()
        a=0
        while stringf[a]!='a':
            if stringf[a+1]!='a':
                if ' '.join(stringf[a:a+2]) in stringdb1:
                    count_match=count_match+2
            else:
                break
            a=a+1
        a=0
        while stringf[a]!='a':
            if stringf[a+1]!='a':
                if stringf[a+2]!='a':
                    if ' '.join(stringf[a:a+3]) in stringdb1:
                        count_match=count_match+3
                else:
                    break
            else:
                break
            a=a+1
        a=0
        if count_match>0:
            if count_match not in arr_p:
                if count_match>arr_p[0]:
                    arr_p.insert(0,count_match)
                    arr_chapter.insert(0,quran.ChapterID)
                    arr_verse.insert(0,quran.VerseID)
                    arr_verse_text.insert(0,' '.join(tmp))
                else:
                    for ind,i in enumerate(arr_p):
                        if count_match>i:
                            arr_p.insert(ind,count_match)
                            arr_chapter.insert(ind,quran.ChapterID)
                            arr_verse.insert(ind,quran.VerseID)
                            arr_verse_text.insert(ind,' '.join(tmp))
                            break
            else:
                for ind,i in enumerate(arr_p):
                    if count_match>i:
                        a=1
                        arr_p.insert(ind,count_match)
                        arr_chapter.insert(ind,quran.ChapterID)
                        arr_verse.insert(ind,quran.VerseID)
                        arr_verse_text.insert(ind,' '.join(tmp))
                        break
                if a==0:
                    arr_p.append(count_match)
                    arr_chapter.append(quran.ChapterID)
                    arr_verse.append(quran.VerseID)
                    arr_verse_text.append(' '.join(tmp))
        stringf.pop()
    context=list(zip(arr_chapter, arr_verse, arr_verse_text))
    return context

def index(request):
    start = time.time()
    if request.method == 'POST':
        if request.POST.get('blob'):
            return HttpResponse(ajax_audio(request.POST.get('blob')))
        elif request.POST['at']!="" and 'file' in request.FILES:
              error='use only one field'
              return render(request,'main_module.html',{'error':error})
        elif request.POST['at']!="":
            file=request.POST['at']
        elif 'file' in request.FILES:
            file=request.FILES['file']
            a=file.content_type
            if a.startswith("text/"):
                file=file.read().decode('utf-8-sig')
            elif a.startswith("image/"):
                file=image_F(file)
            elif a.startswith("audio/"):
                file=audio_F(file)
        else:
            error='input a text or upload a file'
            return render(request,'main_module.html',{'error':error})
        with open('chapters.txt','r',encoding='utf-8') as f:
             c=f.readlines()
        c.insert(0,0)
        context=quran_corrector(file)
        count=len(context)
        end = time.time()
        tm=end - start
        if count==0:
            count=-1
        error1='Sorry,Nothing founds'
        return render(request,'main_module.html',{'context':context,'error1':error1,'file':file,'c':c,'tm':tm,'count':count})
    else:
        return render(request,'main_module.html')