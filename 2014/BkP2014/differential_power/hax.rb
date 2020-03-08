require 'sinatra'
require 'shellwords'

set :public_folder, File.dirname(__FILE__) + '/static'
set :bind, '0.0.0.0'

#get "/u/:username" do
get "/u/" do
    exec = `./graph #{Shellwords.shellescape(params["AAAAAAAAAAAAAAAAA"])}`
    m = exec.split(",")
    str = "var myData = new Array("
    count = 0
    m.each{|ii|
        if ii[1..-1].length == 0
            x = "0"
        else
            x = ii[1..-1]
        end
        s = "[#{count},#{x}],"
        str << s
        count = count + 1
    }
    str = str[0..-2]
    str << ");"

    @data = str
    erb :index
end
