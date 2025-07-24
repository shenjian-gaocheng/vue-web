namespace API.Models;

public class Stage
{
    public int Id { get; set; }
    public int Session { get; set; }
    public string Date { get; set; } = "";
    public string Type { get; set; } = "";
    public string Title { get; set; } = "";
    public string? Url { get; set; }
    public string? CutUrl { get; set; }
    public bool IsStage { get; set; }
    public bool IsEnd { get; set; }
}
