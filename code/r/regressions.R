library(stargazer)
library(reticulate)
library(data.table)

root <- '~/Dropbox/ai_art'
data <- paste0(root, '/data')
tab <- paste0(root, '/tab')

pd <- import('pandas')
panel <- pd$read_pickle(paste0(data, '/daily_data.pkl'))
panel_both <- pd$read_pickle(paste0(data, '/daily_data_both.pkl'))

# Exclude dates before all AI art subreddits existed
panel <- panel[panel$date >= '2022-07-23', ]
panel_both <- panel_both[panel_both$date >= '2022-07-23', ]

# Posts
reg1 <- lm(posts_organic ~ 0 + posts_ai + factor(day_of_week), data = panel)
reg2 <- lm(posts_per_author_organic ~ 0 + posts_per_author_ai + factor(day_of_week), data = panel)
reg3 <- lm(authors_organic ~ 0 + authors_ai + factor(day_of_week), data = panel)
reg4 <- lm(post_score_organic ~ 0 + post_score_ai + factor(day_of_week), data = panel)

# Comments
reg5 <- lm(comments_organic ~ 0 + comments_ai + factor(day_of_week), data = panel)
reg6 <- lm(comments_per_author_organic ~ 0 + comments_per_author_ai + factor(day_of_week), data = panel)
reg7 <- lm(commenters_organic ~ 0 + commenters_ai + factor(day_of_week), data = panel)
reg8 <- lm(comments_per_post_organic ~ 0 + comments_per_post_ai + factor(day_of_week), data = panel)

reg9 <- lm(comments_organic ~ 0 + comments_ai + factor(day_of_week), data = panel_both)
reg10 <- lm(comments_per_author_organic ~ 0 + comments_per_author_ai + factor(day_of_week), data = panel_both)
reg11 <- lm(commenters_organic ~ 0 + commenters_ai + factor(day_of_week), data = panel_both)
reg12 <- lm(comments_per_post_organic ~ 0 + comments_per_post_ai + factor(day_of_week), data = panel_both)

out = stargazer(reg1, reg2, reg3, reg4,
				float = FALSE,
				single.row = TRUE,
				column.sep.width = '1pt',
				keep.stat = c('n', 'rsq'),
				report = 'vc*',
				omit = c('factor*')
)

out = sub('\\caption{}', '', out, fixed = TRUE)
cat(out, sep = '\n',
	file = paste0(tab, '/reg_organic_ai_posts.tex')
)

out = stargazer(reg5, reg6, reg7, reg8,
				float = FALSE,
				single.row = TRUE,
				column.sep.width = '1pt',
				keep.stat = c('n', 'rsq'),
				report = 'vc*',
				omit = c('factor*')
)

out = sub('\\caption{}', '', out, fixed = TRUE)
cat(out, sep = '\n',
	file = paste0(tab, '/reg_organic_ai_comments')
)

out = stargazer(reg9, reg10, reg11, reg12,
				float = FALSE,
				single.row = TRUE,
				column.sep.width = '1pt',
				keep.stat = c('n', 'rsq'),
				report = 'vc*',
				omit = c('factor*')
)

out = sub('\\caption{}', '', out, fixed = TRUE)
cat(out, sep = '\n',
	file = paste0(tab, '/reg_organic_ai_comments_overlapping_commenters')
)

