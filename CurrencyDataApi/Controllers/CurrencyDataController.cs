using Microsoft.AspNetCore.Mvc;
using CurrencyDataApi.Services;

namespace CurrencyDataApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CurrencyDataController : ControllerBase
    {
        private readonly ElasticsearchService _elasticsearchService;

        public CurrencyDataController(ElasticsearchService elasticsearchService)
        {
            _elasticsearchService = elasticsearchService;
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var data = await _elasticsearchService.GetCurrencyDataAsync();
            return Ok(data);
        }
    }
}