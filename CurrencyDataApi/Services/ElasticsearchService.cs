using Elasticsearch.Net;
using Nest;
using CurrencyDataApi.Models;

namespace CurrencyDataApi.Services
{
    public class ElasticsearchService
    {
        private readonly IElasticClient _client;

        public ElasticsearchService()
        {
            var settings = new ConnectionSettings(new Uri("http://localhost:9200"))
                .DefaultIndex("currency_data");
            _client = new ElasticClient(settings);
        }

        public async Task<List<CurrencyData>> GetCurrencyDataAsync()
        {
            var searchResponse = await _client.SearchAsync<CurrencyData>(s => s
                .Query(q => q.MatchAll())
            );

            return searchResponse.Documents.ToList();
        }
    }
}