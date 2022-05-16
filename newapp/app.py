import config as config
import markdown
import os
import fileinput
from bs4 import BeautifulSoup
import tag as Tag
app = config.config
TAGS = app['TAGS']
TAGSFILE = app['TAGSFILE']
TopicsDir = app['TopicsDir']
ArticlesDir = app['ArticlesDir']
TAG_MEMO = {}
ART_MEMO = {}


def add_to_tag_memo():
    """_summary_
    """
    global TAG_MEMO
    tags = get_state()
    for tag in tags:
        newtag = Tag.Tag()
        newtag.set(tag)
        TAG_MEMO[tag] = newtag


def add_to_art_memo():
    """_summary_
    """
    global TAG_MEMO
    TAG_MEMO[0] = []


def get_tagstring(update=True):
    """
    Get tags from tagfile.csv -> str(tags,)
    """
    global TAGS
    if update is False:
        return TAGS
    tags = ''
    with open(TAGSFILE, "r") as tagfile:
        for i in tagfile:
            tags += i+","
    TAGS = tags
    return TAGS


def get_state():
    """get state of tags"""
    return get_tagstring(False)


def add_tag():
    """
    add tag to the taglist and tagfile.csv
    """
    tags = str(input("enter:\t tag or tags sep=space \n"))
    tags = tags.split(" ")
    count = len(get_tagstring())
    for tag in tags:
        print(update_tags([tag, ]))
    return "Added : " + str(len(tags)) + " to " + str(count) + "tagslist"


def md_to_html(md):
    with open(os.path.abspath('docs') + '/' + md + '.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    with open(os.path.abspath('static') + '/' + md + '/index.html', 'w') as f:
        f.write(html)
    return str(html)


def render_temp(template, **params):
    t = app['jinja_env'].get_template(template)
    return t.render(params)


def check_file(file, tag, folder):
    """
    cheek single file for single tag
    """
    for line in fileinput.input(folder + file, inplace=True):
        line = line.replace(tag, "[[" + tag + "]]")
        print(line, end='')


def loop_tags(file, taglist, folder):
    """
    loop tags calling check_file
    """
    print("Looping Tags")
    j = taglist.split(",")
    h = filter(None, j)
    print("checking file: " + file)
    for k in h:
        # print( "for: " + k)
        check_file(file, str(k), folder)


def check_for_tags(Dir):
    """
    Loop through files looking for instances of tag in
    ArticlesDir adding markdown tag ->  tag  to Topic file
    """

    print("Getting Tags")
    tagslist = [x for x in get_tagstring()]
    # print(type(tagslist))
    taglist = str(tagslist[0].split(","))
    # print(type(taglist))
    for filename in os.listdir(Dir):
        if filename.endswith(".md"):
            loop_tags(filename, taglist, Dir)


def check_files_for_tags(folder):
    """
    Loop through files looking for instances of tag in ArticlesDir adding
    markdown tag ->  tag  to Topic file
    """

    print("Getting Tags")
    tagslist = [x for x in get_tagstring()]
    print(type(tagslist))
    taglist = str(tagslist[0].split(","))
    print(type(taglist))
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            loop_tags(filename, taglist, folder)


def create_empty_file_from_tags(folder=TopicsDir):
    """
    Create empty file from tags.csv, ArticlesDir -> Files if not exists
    """

    tagslist = [x for x in get_tagstring()]
    count = 0
    taglist = tagslist[0].split(",")
    for tag in taglist:
        # print('attempting to open', tag)
        with open('./docs/tags/'+tag+".md", "w") as newfile:
            newfile.write("#"+tag)
            count += 1
    print("wrote : ", count, " files to cwd in {0}".format(folder))

    newtaglist = get_tagstring()
    return "Wrote : " + str(len(taglist)) + str(len(newtaglist)) + "to " + \
        ArticlesDir


updatetagfiles = create_empty_file_from_tags(TopicsDir)


def collect_tags_from_filenames():
    tags = []
    for filename in os.listdir(TopicsDir):
        if type(filename) == str and filename.endswith('.md'):
            tag = filename[0:len(filename)-3]+","
            tags += [tag]
        else:
            continue
        # if os.stat(ArticlesDir + "/" + filename).st_size == 0 :
        # print(tag)
        # else:
        # continue
    with open(TAGSFILE, "a") as tagfile:
        print('Writing : ', tags)
        tags = [("," + tag) for tag in tags]
        tagstring = list_to_string(tags)
        tagfile.write(tagstring)


def list_to_string(elements):
    """list to string
    """
    string_elements = ""
    for element in string_elements:
        string_elements += element
    return string_elements


def populate_tagfile_with_tags(TopicsDir, ArticlesDir):
    """
    Loop through topicfolder and add to corresponding tagfile
    articles where tag is found
    """
    topics = [j[0:-3] for j in os.listdir(TopicsDir)]
    articles = [j for j in os.listdir(ArticlesDir) if len(j) > 1]
    for topic in topics:
        artcount = 0
        count = 0
        for article in articles:
            if article.endswith('.md'):
                artcount += 1
                text = open(ArticlesDir + "/" + article, 'r')
                for line in text:
                    if topic in line:
                        count += 1
                        with open(topic + ".md", "a") as topicFile:
                            topicFile.write("#" + topic + "\n")
                            topicFile.write("Article: [[" + article + "]]" +
                                            "\n")
                            break
                    else:
                        continue
                text.close()
            else:
                continue
        print("Found : " + str(count) + " " + topic + "in" + str(artcount) +
              "files")


def update_tags(tags=[]):
    """loop FileDir for new Tags
    """
    if tags == []:
        print('Nothing to add')
        return
    for tag in tags:
        if update_state(tag):
            print('added:' + tag + ' to tags.csv')
        else:
            print("Error: Somehow, Some thing went wrong . . . somwhere. . .")
            return
    return tags


def update_state(toadd=[]):
    """[ get_state -> update_tags(state) ]
    """
    curstate = get_state()
    if toadd in curstate or toadd == []:
        print("Nothing To Add")
        return curstate
    else:
        update = update_tag(toadd, curstate)
    return (curstate != update)


def update_tag(tag, tagslist):
    tags_list = update_tagslist(tag, tagslist)
    with open(TAGSFILE, "a") as tagfile:
        print('Writing: ', tag)
        tagfile.write("," + tag)

    return tags_list


def update_tagslist(tags, tagslist):
    for tag in tags:
        if tag in tagslist:
            tagslist += tag
    return tagslist


def do_tag_thing():
    print(get_state())
    print(update_tags())
    print(updatetagfiles)
    create_empty_file_from_tags(TopicsDir)
    check_files_for_tags(ArticlesDir)
    collect_tags_from_filenames()
    populate_tagfile_with_tags(TopicsDir, ArticlesDir)


def strip_tags(md):
    """Strip tags.

    Args:
        md (md): strip tags

    Returns:
        txt: without tags
    """    # pip install beautifulsoup4

    def md_to_text(md):
        html = markdown.markdown(md)
        soup = BeautifulSoup(html, features='html.parser')
        return soup.get_text()
    return md_to_text(md)


def loop_folder():
    topics = [j[0:-3] for j in os.listdir(ArticlesDir)]
    print('Found : ' + str(len(topics)) + 'files')
    count = 0
    for topic in topics:
        if topic != "":
            md = open(ArticlesDir+topic+".md", 'r')
            text = strip_tags(md.read())
            with open(ArticlesDir+'aaa/' + topic+".md", "w") as topicFile:
                topicFile.write(text)
                count += 1
        return 'Created : ' + str(count) + 'files'


loop_folder()
