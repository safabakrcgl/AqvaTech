using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using CurrencyDataBlazor.Models;

namespace CurrencyDataBlazor.Services
{
    public class CurrencyDataService
    {
        private readonly HttpClient _httpClient;

        public CurrencyDataService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<CurrencyData>> GetCurrencyDataAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<CurrencyData>>("api/currencydata");
        }
    }
}