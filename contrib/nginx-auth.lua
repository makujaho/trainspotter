-- authorization rules

local restrictions = {
  guest  = {
    ["^/$"]                             = { "HEAD" }
  },

  admin = {
    ["^/?[^/]*/?[^/]*/_bulk"]          = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/_refresh"]       = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/?[^/]*/_create"] = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/?[^/]*/_update"] = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/?.*"]            = { "GET", "POST", "PUT", "DELETE" },
    ["^/?[^/]*/?[^/]*$"]               = { "GET", "POST", "PUT", "DELETE" },
    ["/_aliases"]                      = { "GET", "POST" },
    ["^.*$"]                           = { "GET", "POST", "PUT", "DELETE", "HEAD"}
  },

  kibana = {
    ["^/?[^/]*/?[^/]*/_bulk"]          = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/_refresh"]       = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/?[^/]*/_create"] = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/?[^/]*/_update"] = { "GET", "POST" },
    ["^/?[^/]*/?[^/]*/?.*"]            = { "GET", "POST", "PUT" },
    ["^/?[^/]*/?[^/]*$"]               = { "GET", "POST", "PUT" },
    ["/_aliases"]                      = { "GET", "POST" }
  }
}

-- get authenticated user as role
local role = ngx.var.remote_user

-- exit 403 when no matching role has been found
if restrictions[role] == nil then
  ngx.header.content_type = 'text/plain'
  ngx.status = 403
  ngx.say("403 Forbidden: You don't have access to this resource.")
  return ngx.exit(403)
end

-- get URL
local uri = ngx.var.uri

-- get method
local method = ngx.req.get_method()

local allowed  = false

for path, methods in pairs(restrictions[role]) do

  -- path matched rules?
  local p = string.match(uri, path)

  local m = nil

  -- method matched rules?
  for _, _method in pairs(methods) do
    m = m and m or string.match(method, _method)
  end

  if p and m then
    allowed = true
  end
end

if not allowed then
  ngx.header.content_type = 'text/plain'
  ngx.log(ngx.WARN, "Role ["..role.."] not allowed to access the resource ["..method.." "..uri.."]")
  ngx.status = 403
  ngx.say("403 Forbidden: You don't have access to this resource.")
  return ngx.exit(403)
end