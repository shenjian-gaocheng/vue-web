using API.Data;
using API.Models;
using API.Helpers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;

namespace API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly AppDbContext _context;
    private readonly JwtHelper _jwtHelper;

    public AuthController(AppDbContext context, IConfiguration config)
    {
        _context = context;
        _jwtHelper = new JwtHelper(config);
    }

    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginDto dto)
    {
        var user = _context.Users.SingleOrDefault(u => u.Username == dto.Username);
        if (user == null || !user.CheckPassword(dto.Password))
        {
            return Unauthorized(new { message = "用户名或密码错误" });
        }

        var token = _jwtHelper.GenerateToken(user.Username);
        return Ok(new { token });
    }

    [Authorize] // 表示需要 JWT 验证
    [HttpGet("verify")]
    public IActionResult Verify()
    {
        // 取出用户名
        var username = User.Identity?.Name ?? "未知用户";

        return Ok(new
        {
            message = "Token 有效",
            user = username
        });
    }
};

