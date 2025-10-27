from django.contrib import admin
from .models import Category, Post, Heading, PostAnalytics

@admin.register(Category)
class CategotyAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    search_fields = ('name', 'title', 'description', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    list_filter = ('parent',)
    ordering = ('name',)
    readonly_fields = ('id',)


class HeadingInLine(admin.TabularInline):
    model = Heading
    extra = 1
    fields = ('title', 'level', 'order', 'slug') 
    prepopulated_fields = { 'slug': ('title',) }
    ordering = ('order',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'content', 'keywords', 'slug')
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('status', 'category', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = ( 
        ('General Information', {'fields':( 'title', 'description', 'content', 'thumbnail', 'keywords', 'slug', 'category' )}),
        ('Status & Days',       {'fields':( 'status', 'created_at', 'updated_at' ) } ),
    )
    
    inlines = [HeadingInLine]


@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'views', 'impressions', 'clicks', 'click_through_rate', 'avg_time_on_page', )
    search_fields = ('post_title',)
    readonly_fields = ('views', 'impressions', 'clicks', 'click_through_rate', 'avg_time_on_page',)
    
    def post_title(self, obj):
        return obj.post.title
    
    post_title.short_description = 'Post Title'


#
# Esta opcion se comenta debido a que los Headings ya se estan 
# gestionando directamente con el Post
#
# @admin.register(Heading)
# class HeadingAdmin(admin.ModelAdmin):
#     list_display = ('title', 'post', 'level', 'order')
#     search_fields = ('title', 'post__title')
#     list_filter = ('level', 'post')
#     ordering = ('post', 'order')
#     prepopulated_fields = {'slug': ('title',)}