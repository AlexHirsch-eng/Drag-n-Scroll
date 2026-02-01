from django.contrib import admin
from .models import Word, GrammarRule, GrammarExample, WordProgress, ReviewHistory


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['hanzi', 'pinyin', 'translation_ru', 'hsk_level', 'part_of_speech']
    list_filter = ['hsk_level', 'part_of_speech']
    search_fields = ['hanzi', 'pinyin', 'translation_ru', 'translation_kz']


@admin.register(GrammarRule)
class GrammarRuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'pattern', 'hsk_level']
    list_filter = ['hsk_level']
    search_fields = ['title', 'pattern']


@admin.register(GrammarExample)
class GrammarExampleAdmin(admin.ModelAdmin):
    list_display = ['grammar_rule', 'sentence_hanzi', 'order']
    list_filter = ['grammar_rule']
    search_fields = ['sentence_hanzi', 'sentence_pinyin']
    filter_horizontal = ['word_examples']


@admin.register(WordProgress)
class WordProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'srs_level', 'interval_days', 'next_review_date', 'accuracy']
    list_filter = ['srs_level', 'next_review_date']
    search_fields = ['user__username', 'word__hanzi']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReviewHistory)
class ReviewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'quality', 'old_srs_level', 'new_srs_level', 'reviewed_at']
    list_filter = ['quality', 'reviewed_at']
    search_fields = ['user__username', 'word__hanzi']
    readonly_fields = ['created_at']
