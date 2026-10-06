**Listing** - fields
filtered on by search_listing
- id (string)
- title (string)
- description (string)
- category (string)
- style_tags (string[])
- size (string)
- condition (string)
- price (float)
- colors (string[])
- brand (string)
- platform (string)

**Wardrobe** - fields
represents collection of (clothing) items used/passed to suggest_outfit

wardrobe_name: {  
  items: [  
    {  
      an item  
    },  
    {  
      an item  
    }  
  ]  
}  

item: {  
  id (string),  
  name (string),  
  category (string),  
  colors (string[]),  
  style_tags (string[]),  
  notes (string)  
}  

if empty, items: [] is empty