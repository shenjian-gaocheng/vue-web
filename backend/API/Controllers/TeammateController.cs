using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using API.Data;
using API.Models;

namespace API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TeammateController : ControllerBase
{
    private readonly AppDbContext _context;

    public TeammateController(AppDbContext context)
    {
        _context = context;
    }

    // ✅ 查询所有成员（不需要 Token）
    [HttpGet]
    public IActionResult GetAll()
    {
        var teammates = _context.Teammates.ToList();
        return Ok(teammates);
    }

    // ✅ 添加一个成员（需要 Token）
    [Authorize]
    [HttpPost]
    public IActionResult AddOne([FromBody] Teammate teammate)
    {
        _context.Teammates.Add(teammate);
        _context.SaveChanges();

        return Ok(new { message = "队员添加成功" });
    }

    // ✅ 批量添加（需要 Token）
    [Authorize]
    [HttpPost("batch")]
    public IActionResult AddBatch([FromBody] List<Teammate> teammates)
    {
        _context.Teammates.AddRange(teammates);
        _context.SaveChanges();

        return Ok(new { message = $"成功添加 {teammates.Count} 条队员记录" });
    }
}
