function Link(el)
  if el.target:match("^xl:href=") then
    el.target = el.target:gsub("^xl:href=", "")
    el.target = el.target:gsub("^\"", ""):gsub("\"$", "")
  end
  return el
end