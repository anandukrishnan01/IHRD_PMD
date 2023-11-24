from django import forms

class WorldPopulationSearchForm(forms.Form):
    country = forms.CharField(required=False, label='Country')
    min_population = forms.IntegerField(required=False, label='Minimum Population')
    max_population = forms.IntegerField(required=False, label='Maximum Population')
    min_density = forms.FloatField(required=False, label='Minimum Density')
    max_density = forms.FloatField(required=False, label='Maximum Density')
    area = forms.IntegerField(required=False, label='Area')
    landAreaKm = forms.IntegerField(required=False, label='Land Area (km²)')
    cca2 = forms.CharField(required=False, label='Country Code (2)')
    cca3 = forms.CharField(required=False, label='Country Code (3)')
    netChange = forms.IntegerField(required=False, label='Net Change')
    growthRate = forms.FloatField(required=False, label='Growth Rate')
    worldPercentage = forms.FloatField(required=False, label='World Percentage')
    density = forms.FloatField(required=False, label='Density')
    densityMi = forms.FloatField(required=False, label='Density (mi)')
    rank = forms.IntegerField(required=False, label='Rank')
