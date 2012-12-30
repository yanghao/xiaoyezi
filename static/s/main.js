function recover_email(s)
{
        var a,i;
        a = "";
        for (i=0; i < s.length; i++)
                a += String.fromCharCode(s.charCodeAt(i) - 1);
        return a;
}

