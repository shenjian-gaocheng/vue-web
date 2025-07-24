using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using API.Data;
using API.Models;

namespace API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class StageController : ControllerBase
{
    private readonly AppDbContext _context;

    public StageController(AppDbContext context)
    {
        _context = context;
    }

    // ✅ 获取所有演出记录（公开）
    [HttpGet]
    public IActionResult GetAll()
    {
        var stages = _context.Stages.ToList();
        return Ok(stages);
    }

    // ✅ 添加一条记录（需登录）
    [Authorize]
    [HttpPost]
    public IActionResult AddOne([FromBody] Stage stage)
    {
        _context.Stages.Add(stage);
        _context.SaveChanges();

        return Ok(new { message = "演出记录添加成功" });
    }

    // ✅ 更新记录（需登录）
    [Authorize]
    [HttpPut("{id}")]
    public IActionResult Update(int id, [FromBody] Stage updated)
    {
        var stage = _context.Stages.Find(id);
        if (stage == null)
            return NotFound(new { message = "记录不存在" });

        stage.Session = updated.Session;
        stage.Date = updated.Date;
        stage.Type = updated.Type;
        stage.Title = updated.Title;
        stage.Url = updated.Url;
        stage.CutUrl = updated.CutUrl;
        stage.IsStage = updated.IsStage;
        stage.IsEnd = updated.IsEnd;

        _context.SaveChanges();

        return Ok(new { message = "演出记录已更新" });
    }

    // ✅ 批量添加（需登录）
    [Authorize]
    [HttpPost("batch")]
    public IActionResult AddBatch([FromBody] List<Stage> stages)
    {
        _context.Stages.AddRange(stages);
        _context.SaveChanges();

        return Ok(new { message = $"成功添加 {stages.Count} 条演出记录" });
    }
}
