def get_table(database):

    files = []
    col = database.get_data()
    table_head = "<tr><td>Name</td><td>Status</td></tr>"
    files.append(table_head)

    for y in col.find():
        a = "<tr><td>%s</td>"%y['name']
        files.append(a)
        b = "<td>%s</td></tr>"%y['status']
        files.append(b)

    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
                    <html>
                    <head>
                    <meta content="text/html; charset=ISO-8859-1"
                    http-equiv="content-type">
                    <title>File list</title>
                    </head>
                    <body>
                    <table border='1'>
                    %s
                    </table>
                    </body>
                    </html>
                    ''' % files
    return contents
